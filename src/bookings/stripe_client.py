import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(booking):
    amount_in_paise = int(booking.total_amount * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"Bus Booking - {booking.trip.route.route_name}",
                        "description": f"Seats: {','.join(booking.seat_numbers)}",
                    },
                    "unit_amount": amount_in_paise,
                },
                "quantity": 1,
            }
        ],
        success_url=f"{settings.FRONTEND_URL}/bookings/confirmation?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.FRONTEND_URL}/trips/{booking.trip.id}/seats",
        client_reference_id=str(booking.id),
        metadata={
            "booking_id": str(booking.id),
            "booking_reference": booking.booking_reference,
        },
        expires_at=None,
    )

    return session
