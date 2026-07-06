from django.urls import path
from .views import get_available_routes, get_route_details, get_route_stop_details

urlpatterns = [
    path("", get_available_routes, name="get-routes"),
    path("<uuid:route_id>/", get_route_details, name="route-details"),
    path("<uuid:route_id>/stops/", get_route_stop_details, name="route-stops"),
]
