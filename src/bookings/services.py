import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from .models import Booking
from trips.models import Trip


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


@transaction.atomic
def create_booking(*, user, trip_id, seat_count):
    try:
        trip = Trip.objects.select_for_update().get(
            id=trip_id,
            is_active=True,
        )
    except Trip.DoesNotExist:
        raise NotFound("Trip not found.")
    
    if trip.status != Trip.Status.SCHEDULED:
        raise ValidationError("Trip is not available for booking.")
    
    if seat_count <= 0:
        raise ValidationError("Seat count must be greater than 0.")
    
    if seat_count > trip.available_seats:
        raise ValidationError("Not enough seats available.")
    
    total_amount = Decimal(seat_count) * trip.fare

    booking = Booking.objects.create(
        booking_reference=generate_booking_reference(),
        user=user,
        trip=trip,
        seat_count=seat_count,
        total_amount=total_amount,
        status=Booking.Status.CONFIRMED,
    )

    trip.available_seats -= seat_count
    trip.save(update_fields=["available_seats"])

    return booking


def generate_booking_reference():
    return f"BK-{uuid.uuid4().hex[:8].upper()}"
