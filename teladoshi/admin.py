from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import (
    Vendor, GuestStory, Expedition, Stay,
    Fleet, Restaurant, Place, Stopover, ServiceImage
)

# --- INLINES ---


class ServiceImageInline(admin.TabularInline):
    """
    Allows uploading multiple gallery images directly
    within the Service admin page.
    """
    model = ServiceImage
    extra = 3  # Provides 3 empty slots for new images by default
    fields = ('image', 'alt_text')


class GuestStoryInline(admin.TabularInline):
    """Allows managing testimonials directly inside the Service admin page."""
    model = GuestStory
    extra = 1
    fields = ('author', 'content', 'rating')

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
    inlines = [ServiceImageInline, GuestStoryInline]  # Added ServiceImageInline
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
    inlines = [ServiceImageInline, GuestStoryInline]  # Added ServiceImageInline


@admin.register(Fleet)
class FleetAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'vehicle_type', 'transmission', 'price', 'is_active')
    list_filter = ('is_active', 'vendor', 'transmission')
    search_fields = ('name', 'vehicle_type')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]  # Added ServiceImageInline for car details


@admin.register(Restaurant)
class RestaurantAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'location', 'price', 'is_active')
    list_filter = ('is_active', 'vendor')
    search_fields = ('name', 'location', 'subtitle')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline, GuestStoryInline]  # Added ServiceImageInline


@admin.register(Place)
class PlaceAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'access_type', 'is_active')
    list_filter = ('is_active', 'vendor')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceImageInline]  # Added ServiceImageInline for location photos


@admin.register(Stopover)
class StopoverAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'vendor', 'arrival_city', 'price', 'is_active')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GuestStory)
class GuestStoryAdmin(TabbedTranslationAdmin):
    list_display = ('author', 'rating', 'get_linked_service')
    list_filter = ('rating',)

    def get_linked_service(self, obj):
        return obj.expedition or obj.stay or obj.restaurant
    get_linked_service.short_description = 'Linked Service'

# Optional: Register ServiceImage separately if needed for bulk edits


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text', 'expedition', 'stay', 'restaurant', 'fleet')
