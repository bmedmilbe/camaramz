# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'expeditions', ExpeditionViewSet)
router.register(r'stays', StayViewSet)
router.register(r'fleet', FleetViewSet)
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
