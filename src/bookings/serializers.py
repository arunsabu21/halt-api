from rest_framework import serializers
from .models import Booking, Passenger
from trips.models import Trip


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


class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = [
            "id",
            "seat_number",
            "full_name",
            "age",
            "gender",
            "status",
        ]


class BookingListSerializer(serializers.ModelSerializer):
    route = serializers.CharField(source="trip.route.route_name")
    travel_date = serializers.DateField(source="trip.travel_date")
    active_passenger_count = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_reference",
            "route",
            "travel_date",
            "status",
            "seat_count",
            "active_passenger_count",
            "total_amount",
            "created_at",
        ]

    def get_active_passenger_count(self, obj):
        return obj.passenger_details.filter(status=Passenger.Status.ACTIVE).count()


class BookingSerializer(serializers.ModelSerializer):
    route = serializers.CharField(source="trip.route.route_name")
    travel_date = serializers.DateField(source="trip.travel_date")
    departure_time = serializers.TimeField(source="trip.departure_time")
    arrival_time = serializers.TimeField(source="trip.arrival_time")
    net_paid = serializers.SerializerMethodField()
    passenger_details = PassengerDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_reference",
            "route",
            "travel_date",
            "departure_time",
            "arrival_time",
            "boarding_point",
            "drop_point",
            "status",
            "seat_count",
            "total_amount",
            "refunded_amount",
            "net_paid",
            "passenger_details",
            "created_at",
            "updated_at",
        ]

    def get_net_paid(self, obj):
        return obj.total_amount - obj.refunded_amount
