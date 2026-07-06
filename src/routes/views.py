from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import RouteSerializer, RouteStopSerializer
from .services import get_routes, get_route_by_id, get_route_stops


@api_view(["GET"])
@permission_classes([AllowAny])
def get_available_routes(request):

    routes = get_routes()

    serializer = RouteSerializer(routes, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_route_details(request, route_id):

    route = get_route_by_id(route_id)

    serializer = RouteSerializer(route)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_route_stop_details(request, route_id):

    stops = get_route_stops(route_id)

    serializer = RouteStopSerializer(stops, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )
