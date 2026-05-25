from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# --- REUSABLE MEDIA UTILITIES ---


class ServiceImage(models.Model):
    """
    Stores multiple images for a single service to support
    nested gallery URLs dynamically across any catalog type.
    """
    image = models.ImageField(upload_to='services/gallery/%Y/%m/')
    alt_text = models.CharField(max_length=255, blank=True, help_text="SEO friendly description")

    # Generic Link fields that connect this table to any concrete service model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        null=True,
        blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Gallery Image {self.id} ({self.content_type.model})"


# --- MODEL MANAGERS FOR OPTIMIZED DB RETRIEVAL ---

class ServiceManager(models.Manager):
    """Unified manager that automatically handles vendor lookups and prefetches galleries."""

    def get_queryset(self):
        return super().get_queryset().select_related('vendor').prefetch_related('gallery', 'reviews')


# --- VENDOR & ABSTRACT BASE MODEL ---

class Vendor(models.Model):
    """Ties marketplace entities back to a specific operator."""
    company_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='vendors/logos/', null=True, blank=True)

    def __str__(self):
        return self.company_name


class BaseService(models.Model):
    """Abstract model to share common fields across services."""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="%(class)s_services")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='services/covers/%Y/%m/', help_text="Main cover image")
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    # Reverse generic relation shortcut: enables 'service.gallery.all()' everywhere
    gallery = GenericRelation(ServiceImage)
    reviews = GenericRelation('order.Review', related_name='services')
    # Attach the optimized lookup manager to all concrete subclasses
    objects = ServiceManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# --- SPECIFIC CONCRETE SERVICE MODELS ---

class Expedition(BaseService):
    specialization = models.CharField(max_length=255)
    badge_tags = models.CharField(max_length=255)
    mastery_text = models.TextField()


class Stay(BaseService):
    category = models.CharField(max_length=100)
    location_detail = models.CharField(max_length=255)
    amenities = models.TextField()


class Restaurant(BaseService):
    subtitle = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=100)


class Fleet(BaseService):
    vehicle_type = models.CharField(max_length=100)
    transmission = models.CharField(max_length=50, choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')])
    engine = models.CharField(max_length=100)
    features = models.CharField(max_length=255)


class Place(BaseService):
    access_type = models.CharField(max_length=100, default="Free Access")
    coordinates = models.CharField(max_length=100, blank=True)


class Stopover(BaseService):
    arrival_city = models.CharField(max_length=100, default="Lisbon")
    pricing_guide_json = models.JSONField(help_text="Store passenger group rates")
    transfer_details = models.TextField()
