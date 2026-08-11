from celery import shared_task
from django.template.loader import render_to_string

from core.email.resend import send_mail
from .models import Booking, Passenger
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

    attachments = [
        (
            f"ticket_{booking.booking_reference}_{passenger.seat_number}.pdf",
            generate_ticket_pdf(booking, passenger),
        )
        for passenger in booking.passenger_details.all()
    ]

    send_mail(
        to=booking.user.email,
        subject=f"Booking Confirmed - {booking.booking_reference}",
        html=html_content,
        attachments=attachments,
    )


@shared_task
def send_passenger_cancelled_email_task(booking_id, passenger_id, refund_amount):
    try:
        booking = Booking.objects.select_related("trip", "trip__route", "user").get(id=booking_id)
        passenger = booking.passenger_details.get(id=passenger_id)
    except (Booking.DoesNotExist, Passenger.DoesNotExist):
        return

    context = {
        "booking": booking,
        "trip": booking.trip,
        "passenger": passenger,
        "refund_amount": refund_amount,
    }
    html_content = render_to_string("bookings/emails/passenger_cancelled.html", context)

    pdf_bytes = generate_ticket_pdf(booking, passenger)
    attachments = [
        (f"ticket_{booking.booking_reference}_{passenger.seat_number}_cancelled.pdf", pdf_bytes)
    ]

    send_mail(
        to=booking.user.email,
        subject=f"Ticket Cancelled - {booking.booking_reference}",
        html=html_content,
        attachments=attachments,
    )