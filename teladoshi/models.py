from django.db import models
from django.core.validators import MinValueValidator

from django.db import models


class ExpeditionManager(models.Manager):
    def get_queryset(self):
        # Joins Vendor and pre-fetches Gallery + Stories
        return super().get_queryset().select_related('vendor').prefetch_related('gallery', 'stories')


class StayManager(models.Manager):
    def get_queryset(self):
        # Joins Vendor and pre-fetches Gallery + Stories
        return super().get_queryset().select_related('vendor').prefetch_related('gallery', 'stories')


class FleetManager(models.Manager):
    def get_queryset(self):
        # Joins Vendor and pre-fetches Gallery
        return super().get_queryset().select_related('vendor').prefetch_related('gallery')


class RestaurantManager(models.Manager):
    def get_queryset(self):
        # Joins Vendor and pre-fetches Gallery + Stories
        return super().get_queryset().select_related('vendor').prefetch_related('gallery', 'stories')


class PlaceManager(models.Manager):
    def get_queryset(self):
        # Note: Place uses 'images' related_name for its gallery
        return super().get_queryset().select_related('vendor').prefetch_related('images')

# --- NEW: NESTED IMAGE MODEL ---


class ServiceImage(models.Model):
    """
    Stores multiple images for a single service to support
    nested gallery URLs (e.g., /expeditions/1/gallery/).
    """
    image = models.ImageField(upload_to='services/gallery/%Y/%m/')
    alt_text = models.CharField(max_length=255, blank=True, help_text="SEO friendly description")

    # Relationships to enable nested visual logs for each category
    expedition = models.ForeignKey(
        'Expedition', on_delete=models.CASCADE, null=True, blank=True, related_name='gallery'
    )
    stay = models.ForeignKey(
        'Stay', on_delete=models.CASCADE, null=True, blank=True, related_name='gallery'
    )
    restaurant = models.ForeignKey(
        'Restaurant', on_delete=models.CASCADE, null=True, blank=True, related_name='gallery'
    )
    fleet = models.ForeignKey(
        'Fleet', on_delete=models.CASCADE, null=True, blank=True, related_name='gallery'
    )
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Gallery Image {self.id}"

# --- UPDATED BASE MODELS ---


class Vendor(models.Model):
    """Ties marketplace entities back to the specific operator."""
    company_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    contact_email = models.EmailField(blank=True)
    # Added logo for the vendor as seen in "Trusted Guides" section
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

    class Meta:
        abstract = True

# --- SPECIFIC SERVICE MODELS ---


class Expedition(BaseService):
    """Supports 'In the Field' nested galleries."""
    specialization = models.CharField(max_length=255)
    badge_tags = models.CharField(max_length=255)
    mastery_text = models.TextField()
    objects = ExpeditionManager()


class Stay(BaseService):
    """Supports 'The Unseen Mucumbli' visual logs."""
    category = models.CharField(max_length=100)
    location_detail = models.CharField(max_length=255)
    amenities = models.TextField()
    objects = StayManager()
    objects = FleetManager()


class Restaurant(BaseService):
    """Supports 'Through the Lens' food galleries."""
    subtitle = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=100)
    objects = RestaurantManager()


class Fleet(BaseService):
    """Supports car detail galleries."""
    vehicle_type = models.CharField(max_length=100)
    transmission = models.CharField(max_length=50, choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')])
    engine = models.CharField(max_length=100)
    features = models.CharField(max_length=255)
    objects = FleetManager()


class GuestStory(models.Model):
    """Reusable model for the 'Guest Stories' section found on all pages."""
    # Generic foreign key logic could be used here, but for simplicity:
    author = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=5)

    # Links to specific service types
    expedition = models.ForeignKey(
        'Expedition',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='stories')
    stay = models.ForeignKey('Stay', on_delete=models.CASCADE, null=True, blank=True, related_name='stories')
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='stories')


class Place(BaseService):
    """Based on 'Lagoa Azul' page"""
    access_type = models.CharField(max_length=100, default="Free Access")
    coordinates = models.CharField(max_length=100, blank=True)
    objects = PlaceManager()


class Stopover(BaseService):
    """Based on 'Pure Stopover' page"""
    arrival_city = models.CharField(max_length=100, default="Lisbon")
    pricing_guide_json = models.JSONField(help_text="Store 1-4 passengers, 5-8 passengers rates")
    transfer_details = models.TextField()
