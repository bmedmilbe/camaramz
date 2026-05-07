from .models import Client, ClientApp, Domain
from django_tenants.admin import TenantAdminMixin
from django.contrib import admin
from django.http import Http404
from django.conf import settings
from types import MethodType
from . import models
# Register your models here.

from django.contrib.contenttypes.models import ContentType


def _get_request_tenant(request):
    """Resolve the current tenant (Client) from request user or host domain."""
    tenant = getattr(request, 'tenant', None)

    if tenant is not None:
        return tenant

    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated and hasattr(user, 'tenant'):
        return user.tenant

    host = request.get_host().split(':')[0]
    if not host:
        return None

    try:
        domain = Domain.objects.select_related('tenant').get(domain=host)
        return domain.tenant  # This is a Client object
    except Domain.DoesNotExist:
        return None


def _tenant_allowed_app_labels(tenant):
    active_apps = tenant.client_apps.filter(is_active=True).values_list('app', flat=True)
    return {app.rsplit('.', 1)[-1] for app in active_apps}


original_get_app_list = admin.site.get_app_list
original_app_index = admin.site.app_index


def tenant_get_app_list(self, request):
    """Filter admin apps: 'core' only for superusers, others by ClientApp."""
    app_list = original_get_app_list(request)
    tenant = _get_request_tenant(request)
    # 1. Get the set of allowed apps from DB for this tenant
    allowed_app_labels = _tenant_allowed_app_labels(tenant) if tenant else set()

    # 2. Get the list of all apps marked as TENANT_APPS in settings
    tenant_app_labels = {app.rsplit('.', 1)[-1].lower() for app in settings.TENANT_APPS}

    filtered = []
    for app in app_list:
        label = app['app_label'].lower()

        # RULE 1: 'core' app is strictly for superusers only
        if label == 'core':
            if request.user.is_superuser:
                filtered.append(app)
            continue  # Move to next app

        # RULE 2: Superusers see everything else automatically
        if request.user.is_superuser:
            filtered.append(app)
            continue

        # RULE 3: For everyone else, check if it's a shared app or an allowed tenant app
        # If it's NOT a tenant-specific app, show it (e.g. standard Django apps)
        # If it IS a tenant app, it must be in the allowed_app_labels list
        if label not in tenant_app_labels or label in allowed_app_labels:
            filtered.append(app)

    return filtered


def tenant_app_index(self, request, app_label, extra_context=None):
    tenant = _get_request_tenant(request)
    if tenant is not None and not (hasattr(request, 'user') and request.user.is_superuser):
        allowed_labels = _tenant_allowed_app_labels(tenant)
        tenant_app_labels = {app.rsplit('.', 1)[-1] for app in settings.TENANT_APPS}
        if app_label in tenant_app_labels and app_label not in allowed_labels:
            raise Http404
    return original_app_index(request, app_label, extra_context)


admin.site.get_app_list = MethodType(tenant_get_app_list, admin.site)
admin.site.app_index = MethodType(tenant_app_index, admin.site)


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "model", "app_label"]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", 'email', 'tenant']
    search_fields = ["first_name", "last_name",]
    list_editable = ['tenant']
    autocomplete_fields = ['tenant']

    def get_search_results(self, request, queryset, search_term):
        # Create the instance

        # Customize the queryset here (e.g., additional filtering)
        # For demonstration purposes, let's filter books published after 2000
        if not request.user.is_superuser:
            queryset = queryset.filter(parthner=request.user.parthner)

        # Call the parent method to perform the default search
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # pass
            return qs  # Superusers see all records
        return qs.filter(parthner=request.user.parthner)  # Others see only their own records


@admin.register(models.Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ['name']


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', )


@admin.register(ClientApp)
class ClientAppAdmin(admin.ModelAdmin):
    list_display = ('client', 'app', 'is_active')
    autocomplete_fields = ['client']
