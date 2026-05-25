from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

# --- CUSTOMER MANAGEMENT ---


class Customer(models.Model):
    """Simple customer model for checkout process."""
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order_customers'
    )

    def __str__(self):
        return f"Customer: {self.customer.username}"


# --- CART MANAGEMENT ---

class Cart(models.Model):
    """Simple cart model to hold selected services before checkout."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart: {self.id}"


class CartItem(models.Model):
    """Items in the cart, linked to specific services using Generic Foreign Keys."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='cart_items')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    days = models.PositiveIntegerField(default=1)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    people = models.PositiveIntegerField(default=1)
    arrive_flight = models.CharField(max_length=100, null=True, blank=True)
    depart_flight = models.CharField(max_length=100, null=True, blank=True)
    arrive_date = models.DateTimeField(null=True, blank=True)
    depart_date = models.DateTimeField(null=True, blank=True)


# --- BOOKING & ORDER MANAGEMENT ---

class Booking(models.Model):
    """Represents an asynchronous provider request and client checkout link."""
    class BookingStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        AWAITING_SMS = 'Awaiting SMS', _('Awaiting SMS confirmation from vendor')
        SMS_CONFIRMED = 'SMS Confirmed', _('Vendor confirmed via SMS')
        PAYMENT_PENDING = 'Payment Pending', _('Waiting for customer payment')
        CONFIRMED = 'Confirmed', _('Paid & Fully Confirmed')
        CANCELLED = 'Cancelled', _('Cancelled')

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='telabookings')
    status = models.CharField(max_length=30, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    booking_date = models.DateTimeField(auto_now_add=True)

    revolut_payment_url = models.URLField(
        max_length=500, null=True, blank=True,
        help_text="Generated Revolut link sent to customer"
    )
    sms_session_id = models.UUIDField(
        default=uuid4, editable=False, unique=True,
        help_text="Used to pair the android reply back to this booking"
    )

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username} ({self.status})"


class BookingItem(models.Model):
    """Individual service line-items nested within a booking invoice."""
    class ItemStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        CONFIRMED = 'Confirmed', _('Confirmed')
        STARTED = 'Started', _('Started')
        CANCELLED = 'Cancelled', _('Cancelled')
        TERMINATED = 'Terminated', _('Terminated')

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='booking_items')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    days = models.PositiveIntegerField(default=1)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    people = models.PositiveIntegerField(default=1)
    arrive_flight = models.CharField(max_length=100, null=True, blank=True)
    depart_flight = models.CharField(max_length=100, null=True, blank=True)
    arrive_date = models.DateTimeField(null=True, blank=True)
    depart_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.PENDING,
        help_text="Current state of this specific reservation item life-cycle"
    )


class SMSOutgoingQueue(models.Model):
    """
    FIXED: Placed safely below Booking and BookingItem to avoid compilation crashes.
    Android Gateway Polling Table to handle offline STP vendor confirmations.
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='sms_logs')
    phone_number = models.CharField(max_length=30, help_text="Provider's STP number")
    message_text = models.TextField()
    is_sent_by_phone = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS to {self.phone_number} - Sent: {self.is_sent_by_phone}"


# --- FINANCIAL TRANSACTIONS ---

class Payment(models.Model):
    """Simple payment model to track transactions."""
    class PaymentStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        CONFIRMED = 'Confirmed', _('Confirmed')
        FAILED = 'Failed', _('Failed')

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="Current state of the financial payment transaction"
    )


# --- REVIEWS & FEEDBACK ---

class Review(models.Model):
    """Customer reviews for services."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(default=5)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='service_reviews')
    object_id = models.PositiveIntegerField()
    service = GenericForeignKey('content_type', 'object_id')


class GatewayHeartbeat(models.Model):
    """Logs regular connection pings from the Android phone in STP."""
    device_name = models.CharField(max_length=50, default="STP_Phone_Primary")
    last_seen = models.DateTimeField(auto_now=True)
    battery_level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.device_name} - Pinged: {self.last_seen}"
