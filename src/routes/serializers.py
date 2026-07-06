from rest_framework import serializers
from .models import Route, RouteStop


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            "id",
            "route_code",
            "route_name",
            "source_city",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "updated_at",
        ]


class RouteStopSerializer(serializers.ModelSerializer):
    city_id = serializers.UUIDField(source="city.id", read_only=True)
    city = serializers.CharField(source="city.name", read_only=True)
    state = serializers.CharField(source="city.state", read_only=True)
    class Meta:
        model = RouteStop
        fields = [
            "id",
            "city_id",
            "city",
            "state",
            "stop_order",
        ]

        read_only_fields = fields