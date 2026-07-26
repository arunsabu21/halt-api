from django.core.management.base import BaseCommand
from django.db import transaction
from trips.models import Trip
from bookings.models import SeatBooking


class Command(BaseCommand):
    help = (
        "Recalculates available_seats for all trips based on actual SeatBooking counts."
    )

    def handle(self, *args, **options):
        fixed_count = 0

        with transaction.atomic():
            for trip in Trip.objects.select_related("bus").select_for_update():
                booked_count = SeatBooking.objects.filter(trip=trip).count()
                correct_available = trip.bus.total_seats - booked_count

                if trip.available_seats != correct_available:
                    trip.save(update_fields=["available_seats"])
                    fixed_count += 1

        self.stdout.write(self.style.SUCCESS(f"Done, Fixed {fixed_count} trip(s)."))
