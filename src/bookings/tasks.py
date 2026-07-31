from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Booking
from .tickets import generate_ticket_pdf


@shared_task
def send_booking_confirmed_email_task(booking_id):
    try:
        booking = Booking.objects.select_related(
            "trip", "trip__route", "trip__bus", "trip__bus__operator", "user"
        ).get(id=booking_id)
    except Booking.DoesNotExist:
        return

    context = {
        "booking": booking,
        "trip": booking.trip,
        "passengers": booking.passenger_details.all(),
    }

    html_content = render_to_string("bookings/emails/booking_confirmed.html", context)

    email = EmailMultiAlternatives(
        subject=f"Booking Confirmed - {booking.booking_reference}",
        body=f"Your booking {booking.booking_reference} is confirmed.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )
    email.attach_alternative(html_content, "text/html")

    for passenger in booking.passenger_details.all():
        pdf_bytes = generate_ticket_pdf(booking, passenger)
        email.attach(
            f"ticket_{booking.booking_reference}_{passenger.seat_number}.pdf",
            pdf_bytes,
            "application/pdf",
        )

    email.send(fail_silently=False)


@shared_task
def send_booking_cancelled_email(booking_id):
    try:
        booking = Booking.objects.select_related("trip", "trip__route", "user").get(
            id=booking_id
        )
    except Booking.DoesNotExist:
        return

    context = {"booking": booking, "trip": booking.trip}
    html_content = render_to_string("bookings/emails/booking_cancelled.html", context)

    email = EmailMultiAlternatives(
        subject=f"Booking Cancelled - {booking.booking_reference}",
        body=f"Your booking {booking.booking_reference} has been cancelled.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
