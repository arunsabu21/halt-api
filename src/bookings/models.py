import uuid
from django.conf import settings
from django.db import models

from trips.models import Trip


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"
        EXPIRED = "EXPIRED", "Expired"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_reference = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings"
    )
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name="bookings")
    seat_count = models.PositiveSmallIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_checkout_session_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    seat_numbers = models.JSONField(default=list)
    boarding_point = models.CharField(max_length=150, blank=True)
    drop_point = models.CharField(max_length=150, blank=True)
    passengers = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return self.booking_reference


class SeatBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(
        "Booking", on_delete=models.CASCADE, related_name="seat_booking"
    )
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="seat_booking"
    )
    seat_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Seat Booking"
        verbose_name_plural = "Seat Bookings"

        ordering = ["seat_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["trip", "seat_number"],
                name="unique_trip_seat",
            )
        ]

    def __str__(self):
        return f"{self.trip} - {self.seat_number}"


class Passenger(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CANCELLED = "CANCELLED", "Cancelled"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="passenger_details"
    )
    seat_number = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"
        constraints = [
            models.UniqueConstraint(
                fields=["booking", "seat_number"],
                name="unique_booking_seat_passenger",
            )
        ]

    def __str__(self):
        return (
            f"{self.full_name} - {self.seat_number} ({self.booking.booking_reference})"
        )
