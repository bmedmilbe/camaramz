from rest_framework import serializers
from .models import *


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'alt_text']


class GuestStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestStory
        fields = ['author', 'content', 'rating']

# Base Serializer for common fields


class BaseServiceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.company_name')
    is_vendor_verified = serializers.ReadOnlyField(source='vendor.is_verified')
    gallery = ServiceImageSerializer(many=True, read_only=True)
    stories = GuestStorySerializer(many=True, read_only=True)

    class Meta:
        abstract = True


class ExpeditionSerializer(BaseServiceSerializer):
    class Meta:
        model = Expedition
        fields = '__all__'


class StaySerializer(BaseServiceSerializer):
    class Meta:
        model = Stay
        fields = '__all__'


class FleetSerializer(BaseServiceSerializer):
    class Meta:
        model = Fleet
        fields = '__all__'


class RestaurantSerializer(BaseServiceSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
