from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem, Booking, BookingItem, Review, SMSOutgoingQueue

# --- MIXINS ---


class GenericContentTypeSerializerMixin:
    """Helper to convert content_type model string labels to instances cleanly."""
    model_type = serializers.CharField(write_only=True, help_text="e.g. 'expedition', 'stay'")

    def validate_model_type(self, value):
        try:
            return ContentType.objects.get(app_label='marketplace', model=value.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid catalog service type selection.")


# --- CART SERIALIZERS ---

class CartItemSerializer(GenericContentTypeSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id', 'model_type', 'object_id', 'days', 'from_date', 'to_date',
            'people', 'arrive_flight', 'depart_flight', 'arrive_date', 'depart_date'
        ]

    def create(self, validated_data):
        validated_data['content_type'] = validated_data.pop('model_type')
        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']


# --- BOOKING SERIALIZERS ---

class BookingItemSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = BookingItem
        fields = [
            'id', 'service_type', 'object_id', 'days', 'from_date', 'to_date',
            'people', 'arrive_flight', 'depart_flight', 'arrive_date', 'depart_date', 'status'
        ]


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=True)
    customer_username = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        fields = [
            'id', 'customer_username', 'status', 'booking_date',
            'revolut_payment_url', 'sms_session_id', 'items'
        ]


# --- SMS GATEWAY GATE SYSTEM ---

class SMSOutgoingQueueSerializer(serializers.ModelSerializer):
    """Outbound interface serialization required by your Android phone application"""
    class Meta:
        model = SMSOutgoingQueue
        fields = ['id', 'phone_number', 'message_text', 'is_sent_by_phone']


# --- CUSTOMER ACCOUNT REVIEWS ---

class ReviewSerializer(GenericContentTypeSerializerMixin, serializers.ModelSerializer):
    """Handles product feedback loops tied cleanly to Customer models."""
    customer_username = serializers.ReadOnlyField(source='customer.customer.username')

    class Meta:
        model = Review
        fields = ['id', 'customer_username', 'content', 'rating', 'model_type', 'object_id']
        read_only_fields = ['customer']

    def create(self, validated_data):
        validated_data['content_type'] = validated_data.pop('model_type')
        return super().create(validated_data)
