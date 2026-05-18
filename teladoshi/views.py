from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

# FIX 1: Corrected relative imports from your own marketplace app package
from .models import Expedition, Stay, Fleet, Restaurant, Place, Stopover
from .serializers import ExpeditionSerializer, StaySerializer, FleetSerializer, RestaurantSerializer


class ExpeditionViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'In the Field' logic for specialized guided excursions."""
    # FIX 2 & 3: Uses centralized model manager and removed deleted 'stories' reference
    queryset = Expedition.objects.filter(is_active=True)
    serializer_class = ExpeditionSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'specialization', 'badge_tags']


class StayViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'Eco Sanctuaries' lodging and villa listings."""
    queryset = Stay.objects.filter(is_active=True)
    serializer_class = StaySerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'category', 'location_detail']


class FleetViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles transport assets and rental specifications."""
    queryset = Fleet.objects.filter(is_active=True)
    serializer_class = FleetSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'vehicle_type', 'features']


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles dining and culinary experience locations."""
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'subtitle', 'location']
