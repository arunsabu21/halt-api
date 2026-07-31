from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .tickets import generate_ticket_pdf
from .models import Booking, Passenger

from .serializers import (
    BookingListSerializer,
    BookingSerializer,
    BookingInitiateSerializer,
)

from .services import (
    get_bookings,
    get_booking_details,
    initiate_booking,
    get_booking_by_session_id,
    cancel_booking,
)

from .webhooks import handle_stripe_webhook


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_list(request):
    bookings = get_bookings(request.user)

    serializer = BookingListSerializer(bookings, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_details(request, booking_id):
    booking = get_booking_details(user=request.user, booking_id=booking_id)

    serializer = BookingSerializer(booking)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_initiate(request):
    serializer = BookingInitiateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    checkout_url = initiate_booking(
        user=request.user,
        trip_id=serializer.validated_data["trip"].id,
        seat_numbers=serializer.validated_data["seat_numbers"],
        boarding_point=serializer.validated_data["boarding_point"],
        drop_point=serializer.validated_data["drop_point"],
        passengers=serializer.validated_data["passengers"],
    )

    return Response(
        {"checkout_url": checkout_url},
        status=status.HTTP_201_CREATED,
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def booking_cancel(request, booking_id):
    cancel = cancel_booking(user=request.user, booking_id=booking_id)

    serializer = BookingSerializer(cancel)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook_view(request):
    return handle_stripe_webhook(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_by_session(request):
    session_id = request.query_params.get("session_id")
    if not session_id:
        return Response(
            {"detail": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    booking = get_booking_by_session_id(user=request.user, session_id=session_id)
    serializer = BookingSerializer(booking)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_ticket(request, booking_id, passenger_id):
    booking = get_booking_details(user=request.user, booking_id=booking_id)

    if booking.status != Booking.Status.CONFIRMED:
        return Response(
            {"detail": "Ticket is only available for confirmed bookings."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        passenger = booking.passenger_details.get(id=passenger_id)
    except Passenger.DoesNotExist:
        return Response(
            {"detail": "Passenger not found."}, status=status.HTTP_404_NOT_FOUND
        )

    pdf_bytes = generate_ticket_pdf(booking, passenger)

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="ticket_{booking.booking_reference}_{passenger.seat_number}.pdf"'
    )

    return response
