from django.contrib import admin
from .models import Booking, SeatBooking, Passenger


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "user",
        "trip",
        "seat_count",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "booking_reference",
        "user__email",
        "user__full_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


@admin.register(SeatBooking)
class SeatBookingAdmin(admin.ModelAdmin):
    list_display = (
        "seat_number",
        "booking",
        "trip",
        "created_at",
    )

    list_filter = (
        "trip",
        "created_at",
    )

    search_fields = (
        "seat_number",
        "booking__booking_reference",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = ("seat_number",)


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "booking",
        "seat_number",
        "age",
        "gender",
    )
    list_filter = ("gender",)
    search_fields = (
        "full_name",
        "seat_number",
        "booking__booking_reference",
    )
