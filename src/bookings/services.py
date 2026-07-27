import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from .models import Booking, SeatBooking
from trips.models import Trip
from trips.services import _generate_deck_seats
from .holds import get_held_seats, place_holds, release_holds
from .stripe_client import create_stripe_checkout_session


def get_bookings(user):
    return (
        Booking.objects.select_related(
            "trip",
            "trip__route",
        )
        .filter(user=user)
        .order_by("-created_at")
    )


def get_booking_details(user, booking_id):
    try:
        return Booking.objects.select_related(
            "trip",
            "trip__route",
        ).get(id=booking_id, user=user)

    except Booking.DoesNotExist:
        raise NotFound("Booking not found.")


def _get_valid_seat_numbers(bus):
    if bus.deck_count == bus.Deck.DOUBLE:
        half = bus.total_seats // 2
        lower_count = half
        upper_count = bus.total_seats - half
        return set(
            _generate_deck_seats("L", lower_count, bus.seat_layout)
            + _generate_deck_seats("U", upper_count, bus.seat_layout)
        )
    return set(_generate_deck_seats("S", bus.total_seats, bus.seat_layout))


def generate_booking_reference():
    while True:
        reference = f"BK-{uuid.uuid4().hex[:8].upper()}"

        if not Booking.objects.filter(booking_reference=reference).exists():
            return reference


@transaction.atomic()
def initiate_booking(*, user, trip_id, seat_numbers):
    try:
        trip = Trip.objects.select_for_update().get(id=trip_id, is_active=True)
    except Trip.DoesNotExist:
        raise NotFound("Trip not found.")

    if trip.status != Trip.Status.SCHEDULED:
        raise ValidationError("Trip is not available for booking.")

    seat_count = len(seat_numbers)

    if seat_count == 0:
        raise ValidationError("Select at least one seat.")

    if len(seat_numbers) != len(set(seat_numbers)):
        raise ValidationError("Duplicate seat numbers in request.")

    valid_seats = _get_valid_seat_numbers(trip.bus)
    invalid_seats = [s for s in seat_numbers if s not in valid_seats]

    if invalid_seats:
        raise ValidationError(f"Invalid seat number(s): {','.join(invalid_seats)}")

    booked_seats = set(
        SeatBooking.objects.filter(trip=trip, seat_number__in=seat_numbers).values_list(
            "seat_number", flat=True
        )
    )

    if booked_seats:
        raise ValidationError(
            f"Seat(s) already booked: {','.join(sorted(booked_seats))}"
        )

    held_seats = get_held_seats(trip.id, seat_numbers)

    if held_seats:
        raise ValidationError(
            f"Seat(s) currently held by another customer: {','.join(sorted(held_seats))}"
        )

    if seat_count > trip.available_seats:
        raise ValidationError("Not enough seats available")

    total_amount = Decimal(seat_count) * trip.fare

    booking = Booking.objects.create(
        booking_reference=generate_booking_reference(),
        user=user,
        trip=trip,
        seat_count=seat_count,
        seat_numbers=seat_numbers,
        total_amount=total_amount,
        status=Booking.Status.PENDING,
    )

    if not place_holds(trip.id, seat_numbers, booking.id):
        booking.delete()
        raise ValidationError("One or more seats were jus taken, Please try again.")

    try:
        checkout_session = create_stripe_checkout_session(booking)
    except Exception:
        release_holds(trip.id, seat_numbers)
        booking.delete()
        raise ValidationError("Could not start payment. Please try again.")

    booking.stripe_checkout_session_id = checkout_session.id
    booking.save(update_fields=["stripe_checkout_session_id"])

    return checkout_session.url


def get_booking_by_session_id(user, session_id):
    try:
        return Booking.objects.select_related("trip", "trip__route").get(
            stripe_checkout_session_id=session_id, user=user
        )
    except Booking.DoesNotExist:
        raise NotFound("Booking not found.")


@transaction.atomic
def cancel_booking(*, user, booking_id):
    try:
        booking = Booking.objects.select_related("trip").get(id=booking_id, user=user)
    except Booking.DoesNotExist:
        raise NotFound("Booking not found.")

    if booking.status == Booking.Status.CANCELLED:
        raise ValidationError("Booking is already cancelled.")

    if booking.trip.status == Trip.Status.COMPLETED:
        raise ValidationError("Completed trips cannot be cancelled.")

    trip = Trip.objects.select_for_update().get(id=booking.trip.id)

    trip.available_seats += booking.seat_count
    trip.save(update_fields=["available_seats"])

    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=["status"])

    SeatBooking.objects.filter(booking=booking).delete()

    return booking
