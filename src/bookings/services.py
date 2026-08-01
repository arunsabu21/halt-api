import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError
from datetime import datetime, timedelta
from django.utils import timezone

from .models import Booking, SeatBooking, Passenger
from trips.models import Trip
from trips.services import _generate_deck_seats
from routes.services import get_route_stops
from .holds import get_held_seats, place_holds, release_holds
from .stripe_client import create_stripe_checkout_session, refund_partial_payment
from .tasks import send_passenger_cancelled_email_task


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


def _get_ordered_stop_names(route):
    result = get_route_stops(route.id)
    names = [result["source_city"]]
    names += [stop.city.name for stop in result["stops"]]
    names.append(result["destination_city"])
    return names


def _validate_stops(route, boarding_point, drop_point):
    ordered_names = _get_ordered_stop_names(route)

    if boarding_point not in ordered_names:
        raise ValidationError("Invalid boarding point.")

    if drop_point not in ordered_names:
        raise ValidationError("Invalid drop point.")

    boarding_index = ordered_names.index(boarding_point)
    drop_index = ordered_names.index(drop_point)

    if drop_index <= boarding_index:
        raise ValidationError("Drop point must come after the boarding point.")


def _validate_passengers(seat_numbers, passengers):
    if len(passengers) != len(seat_numbers):
        raise ValidationError("Each selected seat must have exactly passenger.")

    passenger_seats = {p["seat_number"] for p in passengers}

    if passenger_seats != set(seat_numbers):
        raise ValidationError("Passenger seat numbers must match selected seats.")

    for p in passengers:
        if not p.get("full_name", "").strip():
            raise ValidationError("Passenger name is required.")

        age = p.get("age")

        if not isinstance(age, int) or age < 1 or age > 120:
            raise ValidationError("Passenger age must be between 1 and 120.")

        if p.get("gender") not in ("MALE", "FEMALE"):
            raise ValidationError("Passenger gender must be MALE or FEMALE.")


def generate_booking_reference():
    while True:
        reference = f"BK-{uuid.uuid4().hex[:8].upper()}"

        if not Booking.objects.filter(booking_reference=reference).exists():
            return reference


@transaction.atomic()
def initiate_booking(*, user, trip_id, seat_numbers, boarding_point, drop_point, passengers):
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

    _validate_stops(trip.route, boarding_point, drop_point)

    _validate_passengers(seat_numbers, passengers)

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
        boarding_point=boarding_point,
        drop_point=drop_point,
        passengers=passengers,
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


def _get_trip_departure_datetime(trip):
    naive_dt = datetime.combine(trip.travel_date, trip.departure_time)
    return timezone.make_aware(naive_dt)


@transaction.atomic()
def cancel_passenger(*, user, booking_id, passenger_id):
    try:
        booking = Booking.objects.select_related("trip").get(
            id=booking_id, user=user
        )
    except Booking.DoesNotExist:
        raise NotFound("Booking not found.")

    if booking.status != Booking.Status.CONFIRMED:
        raise ValidationError("Only confirmed bookings can be cancelled.")

    try:
        passenger = booking.passenger_details.get(id=passenger_id)
    except Passenger.DoesNotExist:
        raise NotFound("Passenger not found.")

    if passenger.status == Passenger.Status.CANCELLED:
        raise ValidationError("This passenger's ticket is already cancelled.")

    departure_dt = _get_trip_departure_datetime(booking.trip)

    if timezone.now() > departure_dt - timedelta(hours=6):
        raise ValidationError("Cancellation is only allowed up to 6 hours before departure.")

    trip = Trip.objects.select_for_update().get(id=booking.trip_id)

    refund_amount = trip.fare

    refund_partial_payment(
        payment_intent_id=booking.stripe_payment_intent_id,
        amount=refund_amount,
    )

    SeatBooking.objects.filter(trip=trip, seat_number=passenger.seat_number).delete()

    passenger.status = Passenger.Status.CANCELLED
    passenger.save(update_fields=["status"])

    booking.refunded_amount += refund_amount
    trip.available_seats += 1
    trip.save(update_fields=["available_seats"])

    remaining_active = booking.passenger_details.filter(
        status=Passenger.Status.ACTIVE
    ).count()

    if remaining_active == 0:
        booking.status = Booking.Status.CANCELLED

    booking.save(update_fields=["refunded_amount", "status"])

    send_passenger_cancelled_email_task.delay(booking.id, passenger.id, str(refund_amount))
    return passenger
