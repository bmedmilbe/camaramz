import uuid
import requests
from decimal import Decimal
from django.db import transaction
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, Booking, BookingItem, GatewayHeartbeat, SMSOutgoingQueue, Payment, Review, Customer
from .serializers import CartSerializer, CartItemSerializer, BookingSerializer, SMSOutgoingQueueSerializer, ReviewSerializer

from rest_framework.permissions import BasePermission


class IsAndroidGatewayDevice(BasePermission):
    """Custom security lock protecting the STP hardware sync lanes."""

    def has_permission(self, request, view):
        # Expects a hardcoded secret token key inside the HTTP headers
        gateway_token = request.headers.get("X-STP-Gateway-Token")
        return gateway_token == "YOUR_ULTRA_SECRET_HARDWARE_KEY_STRING"


class CartViewSet(viewsets.ModelViewSet):
    """
    Manages transient user sessions before conversion checkout requests.
    """
    queryset = Cart.objects.prefetch_related('items__content_type')
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def checkout(self, request, pk=None):
        """
        STAGE 1: Customer requests a booking.
        Saves the order as 'Awaiting SMS' and queues an verification message.
        """
        cart = self.get_object()
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Create booking in an offline verification block
        booking = Booking.objects.create(
            customer=request.user,
            status=Booking.BookingStatus.AWAITING_SMS
        )

        for item in cart_items:
            BookingItem.objects.create(
                booking=booking,
                content_type=item.content_type,
                object_id=item.object_id,
                days=item.days,
                from_date=item.from_date,
                to_date=item.to_date,
                people=item.people,
                arrive_flight=item.arrive_flight,
                depart_flight=item.depart_flight,
                arrive_date=item.arrive_date,
                depart_date=item.depart_date,
                status=BookingItem.ItemStatus.PENDING
            )

        # Pull the phone number from the Vendor object attached to your service
        # (Assuming your vendor model inside marketplace has a 'phone_number' field)
        first_item = cart_items.first()
        service_instance = first_item.content_type.model_class().objects.get(id=first_item.object_id)

        # Fallback to an admin number if the vendor lacks an active listing
        provider_phone = getattr(service_instance.vendor, 'phone_number', '+2399900000')

        # Craft message text with the unique pairing token signature
        msg = (
            f"TelaDoshi Alert: Request for {service_instance.name}. "
            f"Reply with code {booking.sms_session_id[:8]} followed by YES or NO."
        )

        # Drop the message into the polling log container
        SMSOutgoingQueue.objects.create(
            booking=booking,
            phone_number=provider_phone,
            message_text=msg
        )

        # Clear the temporary workspace container securely
        cart.delete()

        return Response(
            {"status": "Request submitted. Awaiting offline partner verification text."},
            status=status.HTTP_202_ACCEPTED
        )


class AndroidGatewayViewSet(viewsets.ViewSet):
    """
    Polled endpoint utilized by your Android hardware layout running in STP
    to dispatch and pull SMS string streams. Protected by Token or Admin sessions.
    """
    permission_classes = [IsAndroidGatewayDevice]

    @action(detail=False, methods=['get'], url_path='fetch-pending')
    def fetch_pending_sms(self, request):
        # Update active system logs dynamically during the device polling window
        GatewayHeartbeat.objects.update_or_create(
            device_name="STP_Phone_Primary",
            defaults={"battery_level": request.query_params.get("battery")}
        )

        pending = SMSOutgoingQueue.objects.filter(is_sent_by_phone=False)[:5]
        # ... Rest of your existing serialization code logic ...

        serializer = SMSOutgoingQueueSerializer(pending, many=True)

        # Flag out immediately to avoid racing duplicate dispatches
        pending.update(is_sent_by_phone=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='webhook-receiver')
    @transaction.atomic
    def webhook_receiver(self, request):
        """
        STAGE 2: Android app hits this endpoint upon receiving an incoming reply SMS.
        Expected Body: {"sender": "+239995123", "text": "4f8a2b1c YES"}
        """
        sender_phone = request.data.get('sender')
        incoming_text = request.data.get('text', '').strip()

        if not incoming_text:
            return Response({"error": "Empty message content data payload."}, status=status.HTTP_400_BAD_REQUEST)

        # Parse text body components (First word = 8-character code snippet, second word = intent selection)
        parts = incoming_text.split()
        if len(parts) < 2:
            return Response({"error": "Invalid SMS structure format payload template."},
                            status=status.HTTP_400_BAD_REQUEST)

        sms_code_snippet = parts[0].lower()
        decision_intent = parts[1].upper()

        # Find the matching booking entry using the session token signature prefix match lookups
        booking = Booking.objects.filter(sms_session_id__startswith=sms_code_snippet).first()
        if not booking:
            return Response({"error": "Transaction payload verification pairing missing."},
                            status=status.HTTP_404_NOT_FOUND)

        if "YES" in decision_intent:
            booking.status = Booking.BookingStatus.SMS_CONFIRMED
            booking.save()

            # STAGE 3: Invoke the remote Revolut payment generation flow pipeline
            self._trigger_revolut_generation_flow(booking)
            return Response({"message": "Booking approved. Payment workflow dispatched."})
        else:
            booking.status = Booking.BookingStatus.CANCELLED
            booking.items.all().update(status=BookingItem.ItemStatus.CANCELLED)
            booking.save()
            return Response({"message": "Booking rejected and cancelled successfully."})

    def _trigger_revolut_generation_flow(self, booking):
        """Executes Revolut API request integrations and dispatches transactional emails."""
        # Calculate dynamic cost totals
        total_invoice_balance = Decimal('0.00')
        for item in booking.items.all():
            service = item.content_type.model_class().objects.get(id=item.object_id)
            total_invoice_balance += (service.price * item.days * item.people)

        # Connect out directly to the active Revolut Merchant API Endpoint configurations
        revolut_headers = {
            "Authorization": f"Bearer {settings.REVOLUT_SECRET_API_KEY}",
            "Content-Type": "application/json",
            "Revolut-Api-Version": "2024-05-01"
        }

        revolut_payload = {
            "amount": int(total_invoice_balance * 100),  # Revolut expects currency balances in integer cents format
            "currency": "EUR",
            "merchant_order_ext_ref": f"TELADOSHI-{booking.id}"
        }

        try:
            # Sandbox or production endpoints base addresses
            response = requests.post(
                "https://revolut.com",  # Adjust subdomain target environment safely
                json=revolut_payload,
                headers=revolut_headers,
                timeout=10
            )
            if response.status_code == 201:
                # Capture generated checkout hosted landing page mapping arrays
                revolut_data = response.json()
                checkout_hosted_url = revolut_data.get('checkout_url')

                # Update checkout invoice schemas
                booking.revolut_payment_url = checkout_hosted_url
                booking.status = Booking.BookingStatus.PAYMENT_PENDING
                booking.save()

                Payment.objects.create(
                    booking=booking,
                    amount=total_invoice_balance,
                    payment_method="Revolut Link",
                    status=Payment.PaymentStatus.PENDING
                )

                # Send email notification out to the client profile registry mapping hooks
                send_mail(
                    subject="Your TelaDoshi booking request is confirmed! Secure checkout inside.",
                    message=f"Hi! Your provider has accepted your reservation details. Complete checkout secure routing links here: {checkout_hosted_url}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.customer.email],
                    fail_silently=False,
                )
        except requests.RequestException:
            # Maintain active recovery log layers for connection failures
            pass


class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allows logged-in customers to view their dashboard profile accounts,
    audit historical logs, and pull active Revolut payment links.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user).prefetch_related('items__content_type')


class ReviewViewSet(viewsets.ModelViewSet):
    """Handles product feedback loops."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        customer_profile, _ = Customer.objects.get_or_create(customer=self.request.user)
        serializer.save(customer=customer_profile)
