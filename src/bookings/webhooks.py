import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

from .models import Booking, SeatBooking, Passenger
from .holds import release_holds
from trips.models import Trip


def handle_stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return Response(
            {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
        )
    except stripe.error.SignatureVerificationError:
        return Response(
            {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
        )

    event_type = event["type"]
    session = event["data"]["object"]

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(session)

    elif event_type == "checkout.session.expired":
        _handle_checkout_expired(session)

    return Response(status=status.HTTP_200_OK)


@transaction.atomic()
def _handle_checkout_completed(session):
    try:
        booking = Booking.objects.select_for_update().get(
            stripe_checkout_session_id=session["id"]
        )
    except Booking.DoesNotExist:
        return

    if booking.status != Booking.Status.PENDING:
        return

    trip = Trip.objects.select_for_update().get(id=booking.trip.id)

    already_booked = set(
        SeatBooking.objects.filter(
            trip=trip, seat_number__in=booking.seat_numbers
        ).values_list("seat_number", flat=True)
    )

    if already_booked:
        booking.status = Booking.Status.EXPIRED
        booking.save(update_fields=["status"])
        release_holds(trip.id, booking.seat_numbers)
        _refund_booking(booking)
        return

    if booking.seat_count > trip.available_seats:
        booking.status = Booking.Status.EXPIRED
        booking.save(update_fields=["status"])
        release_holds(trip.id, booking.seat_numbers)
        _refund_booking(booking)
        return

    Passenger.objects.bulk_create(
        [
            Passenger(
                booking=booking,
                seat_number=p["seat_number"],
                full_name=p["full_name"],
                age=p["age"],
                gender=p["gender"],
            )
            for p in booking.passengers
        ]
    )

    booking.status = Booking.Status.CONFIRMED
    booking.stripe_payment_intent_id = (
        session["payment_intent"] if "payment_intent" in session else ""
    )
    booking.save(update_fields=["status", "stripe_payment_intent_id"])

    trip.available_seats -= booking.seat_count
    trip.save(update_fields=["available_seats"])

    release_holds(trip.id, booking.seat_numbers)


def _handle_checkout_expired(session):
    try:
        booking = Booking.objects.get(stripe_checkout_session_id=session["id"])
    except Booking.DoesNotExist:
        return

    if booking.status == Booking.Status.PENDING:
        booking.status = Booking.Status.EXPIRED
        booking.save(update_fields=["status"])
        release_holds(booking.trip_id, booking.seat_numbers)


def _refund_booking(booking):
    if booking.stripe_payment_intent_id:
        stripe.Refund.create(payment_intent=booking.stripe_payment_intent_id)
