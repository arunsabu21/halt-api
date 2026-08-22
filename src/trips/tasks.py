from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from routes.models import Route
from buses.models import Bus
from .models import Trip

TRIP_TEMPLATES = [
    {
        "route_code": "RT-CHN-BLR",
        "bus_number": "KSRTC301",
        "departure_time": "21:00:00",
        "arrival_time": "05:30:00",
        "fare": 850.00,
    }
]

DAYS_AHEAD = 30


@shared_task
def ensure_upcoming_trips():
    today = timezone.now().date()

    for template in TRIP_TEMPLATES:
        route = Route.objects.filter(route_code=template["route_code"]).first()
        bus = Bus.objects.filter(bus_number=template["bus_number"]).first()

        if not route or not bus:
            continue

        for offset in range(1, DAYS_AHEAD + 1):
            target_date = today + timedelta(days=offset)
            Trip.objects.get_or_create(
                route=route,
                bus=bus,
                travel_date=target_date,
                defaults={
                    "departure_time": template["departure_time"],
                    "arrival_time": template["arrival_time"],
                    "fare": template["fare"],
                    "available_seats": bus.total_seats,
                    "status": Trip.Status.SCHEDULED,
                    "is_active": True,
                },
            )
