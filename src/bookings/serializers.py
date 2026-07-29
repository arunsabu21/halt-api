from rest_framework import serializers
from .models import Booking
from trips.models import Trip


class BookingListSerializer(serializers.ModelSerializer):
    trip = serializers.CharField(source="trip.route.route_name")
    user = serializers.CharField(source="user.email")
    seat_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_reference",
            "user",
            "trip",
            "seat_count",
            "seat_numbers",
            "total_amount",
            "status",
        ]

    def get_seat_numbers(self, obj):
        return list(
            obj.seat_booking.values_list(
                "seat_number",
                flat=True,
            )
        )


class BookingSerializer(serializers.ModelSerializer):
    trip = serializers.CharField(source="trip.route.route_name")
    user = serializers.CharField(source="user.email")
    seat_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_reference",
            "user",
            "trip",
            "seat_count",
            "seat_numbers",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "booking_reference",
            "user",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_seat_numbers(self, obj):
        return list(
            obj.seat_booking.values_list(
                "seat_number",
                flat=True,
            )
        )


class PassengerInputSerializer(serializers.Serializer):
    seat_number = serializers.CharField()
    full_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=1, max_value=120)
    gender = serializers.ChoiceField(choices=["MALE", "FEMALE"])


class BookingInitiateSerializer(serializers.Serializer):
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.filter(is_active=True)
    )
    seat_numbers = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
    boarding_point = serializers.CharField()
    drop_point = serializers.CharField()
    passengers = PassengerInputSerializer(many=True)
