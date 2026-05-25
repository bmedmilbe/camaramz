from modeltranslation.translator import register, TranslationOptions
from .models import Expedition, Stay, Fleet, Restaurant, Place, Stopover


@register(Expedition)
class ExpeditionTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ('name', 'description', 'specialization', 'mastery_text')


@register(Stay)
class StayTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ('name', 'description', 'category', 'location_detail', 'amenities')


@register(Fleet)
class FleetTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ('name', 'description')


@register(Restaurant)
class RestaurantTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ('name', 'description', 'subtitle', 'location')


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Stopover)
class StopoverTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'transfer_details')
