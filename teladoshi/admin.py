from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline  # MANDATORY FOR GENERIC LINKS
from modeltranslation.admin import TabbedTranslationAdmin
from .models import (
    Vendor, Expedition, Stay,
    Fleet, Restaurant, Place, Stopover, ServiceImage
)

# --- GENERIC INLINES ---


class ServiceImageInline(GenericTabularInline):
    """
    Allows uploading multiple gallery images directly within
    ANY Service admin page using the ContentTypes framework.
    """
    model = ServiceImage
    extra = 3  # Provides 3 empty slots for new images by default
    fields = ('image', 'alt_text')

# --- ADMIN CLASSES ---


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'is_verified', 'contact_email')
    list_filter = ('is_verified',)
    search_fields = ('company_name', 'contact_email')


@admin.register(Expedition)
class ExpeditionAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'price', 'is_active')
    list_filter = ('is_active', 'vendor')
    search_fields = ('name', 'specialization')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]
    fieldsets = (
        ("Core Information", {"fields": ("vendor", "name", "slug", "price", "image", "is_active")}),
        ("Content", {"fields": ("description", "specialization", "badge_tags", "mastery_text")}),
    )


@admin.register(Stay)
class StayAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'is_active')
    list_filter = ('is_active', 'vendor', 'category')
    search_fields = ('name', 'location_detail')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]


@admin.register(Fleet)
class FleetAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'vehicle_type', 'transmission', 'price', 'is_active')
    list_filter = ('is_active', 'vendor', 'transmission')
    search_fields = ('name', 'vehicle_type')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]


@admin.register(Restaurant)
class RestaurantAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'location', 'price', 'is_active')
    list_filter = ('is_active', 'vendor')
    search_fields = ('name', 'location', 'subtitle')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]


@admin.register(Place)
class PlaceAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'access_type', 'is_active')
    list_filter = ('is_active', 'vendor')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]


@admin.register(Stopover)
class StopoverAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'arrival_city', 'price', 'is_active')
    prepopulated_fields = {"slug": ("name",)}


# --- OPTIONAL BULK MEDIA VIEW ---

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    # FIX: Replaced explicit service fields with generic tracking columns
    list_display = ('id', 'alt_text', 'content_type', 'object_id', 'content_object')
    list_filter = ('content_type',)
    search_fields = ('alt_text',)
