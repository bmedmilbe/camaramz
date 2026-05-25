from django.contrib import admin

from .models import (
    Association, AssociationImages, Video, Budget, District,
    ExtraDoc, ExtraImages, Tour, ImagesTour, Post, PostDocument,
    PostFile, PostImage, PostVideo, Information, Role, Team,
    Secretary, Section, SecreatarySection, Partner, Message, YearGoals,
    President, Party, Law, Vote, Customer
)


class AssociationImagesInline(admin.TabularInline):
    model = AssociationImages
    extra = 1
    fields = ['image', 'tenant']


class ExtraImagesInline(admin.TabularInline):
    model = ExtraImages
    extra = 1
    fields = ['picture', 'tenant']


class ImagesTourInline(admin.TabularInline):
    model = ImagesTour
    extra = 1
    fields = ['image', 'tenant']


class PostDocumentInline(admin.TabularInline):
    model = PostDocument
    extra = 1
    fields = ['document', 'tenant']


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1
    fields = ['file', 'tenant']


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['picture', 'tenant']


class PostVideoInline(admin.TabularInline):
    model = PostVideo
    extra = 1
    fields = ['video', 'tenant']


class InformationInline(admin.TabularInline):
    model = Information
    extra = 1
    fields = ['question', 'information', 'tenant']


class SecreatarySectionInline(admin.TabularInline):
    model = SecreatarySection
    extra = 1
    fields = ['section', 'tenant']

# --- ADMIN CLASSES ---


class BaseTenantAdmin(admin.ModelAdmin):
    """
    Base class to handle multi-tenancy in Admin.
    Filters querysets by tenant and auto-assigns tenant on save.
    Hides tenant field from regular users, shows only for superusers.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant=request.user.tenant)

    def save_model(self, request, obj, form, change):
        if not obj.tenant_id and not request.user.is_superuser:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if not request.user.is_superuser:
            # Remove 'tenant' from list_display for regular users
            list_display = [field for field in list_display if field != 'tenant']
        return list_display

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Remove tenant field from form for regular users
            if 'tenant' in form.base_fields:
                del form.base_fields['tenant']
        return form


@admin.register(Association)
class AssociationAdmin(BaseTenantAdmin):
    list_display = ['name', 'district', 'tenant']
    inlines = [AssociationImagesInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user", "backstaff"]
    ordering = ["user"]
    list_editable = ["backstaff"]


@admin.register(Post)
class PostAdmin(BaseTenantAdmin):
    list_display = ['title', 'active', 'featured', 'is_a_service', 'tenant']
    list_filter = ['active', 'is_a_service', 'is_social_service']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['processed_text_file']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'picture', 'text_file')
        }),
        ('Status', {
            'fields': ('active', 'featured', 'is_a_service', 'is_social_service', 'is_to_front')
        }),
        ('Processed Content', {
            'fields': ('processed_text_file',),
            'description': 'Auto-generated JSON file with processed HTML content'
        }),
    )
    inlines = [PostImageInline, PostDocumentInline, PostVideoInline, InformationInline, PostFileInline]


@admin.register(ExtraDoc)
class ExtraDocAdmin(BaseTenantAdmin):
    list_display = ['title', 'active', 'date', 'tenant']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ExtraImagesInline]


@admin.register(Tour)
class TourAdmin(BaseTenantAdmin):
    list_display = ['title', 'active', 'date', 'tenant']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ImagesTourInline]


@admin.register(Secretary)
class SecretaryAdmin(BaseTenantAdmin):
    list_display = ['user', 'tenant']
    inlines = [SecreatarySectionInline]


@admin.register(Budget)
class BudgetAdmin(BaseTenantAdmin):
    list_display = ['title', 'type', 'year', 'tenant']
    list_filter = ['type', 'year']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Team)
class TeamAdmin(BaseTenantAdmin):
    list_display = ['name', 'role', 'from_assembly', 'tenant']
    list_filter = ['from_assembly', 'role']


@admin.register(Video)
class VideoAdmin(BaseTenantAdmin):
    list_display = ['title', 'is_band', 'is_spot', 'created_at', 'tenant']


@admin.register(Message)
class MessageAdmin(BaseTenantAdmin):
    list_display = ['subject', 'name', 'email', 'sent', 'date', 'tenant']
    readonly_fields = ['date']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Role)
class RoleAdmin(BaseTenantAdmin):
    list_display = ['title', 'tenant']


@admin.register(Section)
class SectionAdmin(BaseTenantAdmin):
    list_display = ['title', 'tenant']


@admin.register(Partner)
class PartnerAdmin(BaseTenantAdmin):
    list_display = ['title', 'tenant']


@admin.register(YearGoals)
class YearGoalsAdmin(BaseTenantAdmin):
    list_display = ['year', 'associations', 'products', 'tenant']


@admin.register(President)
class PresidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1
    # Use autocomplete to avoid massive dropdowns if Law/Party tables grow large
    autocomplete_fields = ['party']


@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'an_president', 'stp_president', 'tenant')
    list_filter = ('published_date', 'an_president', 'stp_president', 'tenant')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VoteInline]

    def get_queryset(self, request):
        """
        Uses custom 'optimized' QuerySet method to reduce SQL
        queries (JOINs) when loading the list view.
        """
        qs = super().get_queryset(request)
        return qs.optimized()


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('law', 'party', 'votes')
    list_filter = ('party',)
    search_fields = ('law__title', 'party__name')

    def get_queryset(self, request):
        """
        Uses custom 'optimized' QuerySet method for the Vote list view.
        """
        qs = super().get_queryset(request)
        return qs.optimized()
