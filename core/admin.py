from django.contrib import admin
from . import models
# Register your models here.

from django.contrib.contenttypes.models import ContentType



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