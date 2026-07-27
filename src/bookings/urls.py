from django.urls import path
from .views import (
    booking_list,
    booking_details,
    booking_initiate,
    stripe_webhook_view,
    booking_cancel,
)

urlpatterns = [
    path("", booking_list, name="booking-list"),
    path("initiate/", booking_initiate, name="booking-initiate"),
    path("webhook/", stripe_webhook_view, name="stripe-webhook"),
    path("<uuid:booking_id>/", booking_details, name="booking-details"),
    path("<uuid:booking_id>/cancel/", booking_cancel, name="booking-cancel"),
]
