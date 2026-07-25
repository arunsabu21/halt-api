from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import RouteSerializer, RouteStopSerializer
from .services import get_routes, get_route_by_id, get_route_stops

from core.cache.keys import get_routes_list_key, route_stops_key
from core.cache.services import get_cache, set_cache
from core.constants.cache import ROUTE_LIST_CACHE_TIMEOUT, ROUTE_STOPS_CACHE_TIMEOUT


@api_view(["GET"])
@permission_classes([AllowAny])
def get_available_routes(request):
    cache_key = get_routes_list_key()
    cached_response = get_cache(cache_key)

    if cached_response is not None:
        return Response(
            cached_response,
            status=status.HTTP_200_OK,
        )

    routes = get_routes()

    serializer = RouteSerializer(routes, many=True)

    set_cache(
        key=cache_key,
        value=serializer.data,
        timeout=ROUTE_LIST_CACHE_TIMEOUT,
    )

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
    cache_key = route_stops_key(route_id)
    cached_response = get_cache(cache_key)

    if cached_response is not None:
        return Response(cached_response, status=status.HTTP_200_OK)

    result = get_route_stops(route_id)

    response_data = {
        "route_id": result["route_id"],
        "route_name": result["route_name"],
        "source_city": result["source_city"],
        "destination_city": result["destination_city"],
        "stops": RouteStopSerializer(result["stops"], many=True).data,
    }

    set_cache(key=cache_key, value=response_data, timeout=ROUTE_STOPS_CACHE_TIMEOUT)

    return Response(response_data, status=status.HTTP_200_OK)
