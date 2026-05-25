from rest_framework import serializers
from .models import ServiceImage, Expedition, Stay, Fleet, Restaurant

# Adjust the app name string below if your order app directory has a different name
from order.models import Review


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'alt_text']


class CatalogReviewSerializer(serializers.ModelSerializer):
    """Clean serialisation for customer reviews nested inside service responses."""
    customer_name = serializers.ReadOnlyField(source='customer.customer.username')

    class Meta:
        model = Review
        fields = ['id', 'customer_name', 'content', 'rating']


# Base Serializer
class BaseServiceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.company_name')
    is_vendor_verified = serializers.ReadOnlyField(source='vendor.is_verified')
    gallery = ServiceImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        """Fetches all generic reviews assigned to this specific service instance."""
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(obj)
        reviews = Review.objects.filter(content_type=content_type, object_id=obj.id)
        return CatalogReviewSerializer(reviews, many=True).data


class ExpeditionSerializer(BaseServiceSerializer):
    class Meta:
        model = Expedition
        # Added 'reviews' to fields array
        fields = [
            'id', 'vendor_name', 'is_vendor_verified', 'name', 'description',
            'price', 'image', 'is_active', 'slug', 'gallery', 'reviews',
            'specialization', 'badge_tags', 'mastery_text'
        ]


class StaySerializer(BaseServiceSerializer):
    class Meta:
        model = Stay
        # Added 'reviews' to fields array
        fields = [
            'id', 'vendor_name', 'is_vendor_verified', 'name', 'description',
            'price', 'image', 'is_active', 'slug', 'gallery', 'reviews',
            'category', 'location_detail', 'amenities'
        ]


class FleetSerializer(BaseServiceSerializer):
    class Meta:
        model = Fleet
        # Added 'reviews' to fields array
        fields = [
            'id', 'vendor_name', 'is_vendor_verified', 'name', 'description',
            'price', 'image', 'is_active', 'slug', 'gallery', 'reviews',
            'vehicle_type', 'transmission', 'engine', 'features'
        ]


class RestaurantSerializer(BaseServiceSerializer):
    class Meta:
        model = Restaurant
        # Added 'reviews' to fields array
        fields = [
            'id', 'vendor_name', 'is_vendor_verified', 'name', 'description',
            'price', 'image', 'is_active', 'slug', 'gallery', 'reviews',
            'subtitle', 'location', 'opening_hours'
        ]
