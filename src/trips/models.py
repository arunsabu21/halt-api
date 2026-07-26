import uuid
from django.db import models
from buses.models import Bus
from routes.models import Route
from django.core.exceptions import ValidationError as DjangoValidationError


class Trip(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name="trips")
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name="trips")
    travel_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.available_seats is not None and self.bus_id:
            if self.available_seats > self.bus.total_seats:
                raise DjangoValidationError(
                    {
                        "available_seats": "Available seats cannot exceed the bus's total seats."
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["travel_date", "departure_time"]
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def __str__(self):
        return f"{self.route.route_name}" f"{self.travel_date}"
