from django.contrib import admin

from .models import Customer, Transaction

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'boss']
    list_editable = ['boss']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['value', 'description', 'completed_by', 'completed', 'date', 'is_charge']
    list_filter = ['completed', 'is_charge', 'completed_by', 'boss']
    list_editable = ['completed', 'completed_by']
    search_fields = ['description', 'value']
