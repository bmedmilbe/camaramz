from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from teladoshi.models import Expedition, Fleet, Restaurant, Stay
from teladoshi.serializers import ExpeditionSerializer, FleetSerializer, RestaurantSerializer, StaySerializer


class ExpeditionViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'In the Field' logic for guides like Emanuel Santos."""
    queryset = Expedition.objects.filter(is_active=True).select_related('vendor').prefetch_related('gallery', 'stories')
    serializer_class = ExpeditionSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'specialization', 'badge_tags']


class StayViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'Eco Sanctuaries' like Villa Mucumbli."""
    queryset = Stay.objects.filter(is_active=True).prefetch_related('gallery', 'stories')
    serializer_class = StaySerializer
    lookup_field = 'slug'


class FleetViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles technical specs for the Toyota Hilux Adventure."""
    queryset = Fleet.objects.filter(is_active=True).prefetch_related('gallery')
    serializer_class = FleetSerializer
    lookup_field = 'slug'


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'Through the Lens' food galleries for Roça São João."""
    queryset = Restaurant.objects.filter(is_active=True).prefetch_related('gallery', 'stories')
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
