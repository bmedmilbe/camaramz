
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, AndroidGatewayViewSet, BookingViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'sms-gateway', AndroidGatewayViewSet, basename='sms-gateway')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
