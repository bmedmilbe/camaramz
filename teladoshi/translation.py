from modeltranslation.translator import register, TranslationOptions
from .models import Expedition, Stay, Fleet, Restaurant, Place, Stopover, GuestStory


@register(GuestStory)
class GuestStoryTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(Expedition)
class ExpeditionTranslationOptions(TranslationOptions):
    fields = ('description', 'specialization', 'mastery_text')


@register(Stay)
class StayTranslationOptions(TranslationOptions):
    fields = ('description', 'category', 'location_detail', 'amenities')


@register(Fleet)
class FleetTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Restaurant)
class RestaurantTranslationOptions(TranslationOptions):
    fields = ('description', 'subtitle', 'location')


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Stopover)
class StopoverTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'transfer_details')
