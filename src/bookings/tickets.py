from django.template.loader import render_to_string
from weasyprint import HTML


def generate_ticket_pdf(booking, passenger):
    trip = booking.trip
    bus = trip.bus

    html_string = render_to_string(
        "bookings/ticket.html",
        {
            "booking": booking,
            "passenger": passenger,
            "trip": trip,
            "bus": bus,
            "travel_date": trip.travel_date.strftime("%d %b %Y"),
            "departure_time": trip.departure_time.strftime("%I:%M %p"),
            "fare": trip.fare,
            "support_email": bus.operator.support_email,
        },
    )

    pdf_bytes = HTML(string=html_string).write_pdf()
    return pdf_bytes
