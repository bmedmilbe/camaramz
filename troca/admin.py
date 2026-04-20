from django.contrib import admin
from .models import Customer, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Administrative interface for Customer profiles.
    Allows quick promotion of users to 'Boss' status directly from the list view.
    """
    list_display = ['user', 'boss']
    list_editable = ['boss']  # Enable quick status updates without opening the record


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Backoffice dashboard for financial transactions.

    Features:
        - Real-time status filtering (completed vs. pending).
        - Quick-edit capabilities for transaction settlement.
        - Search functionality across descriptions and financial values.
    """
    list_display = ['value', 'description', 'completed_by', 'completed', 'date', 'is_charge']
    list_filter = ['completed', 'is_charge', 'completed_by', 'boss']

    # Allows the Admin/Boss to settle transactions directly from the summary table
    list_editable = ['completed', 'completed_by']

    search_fields = ['description', 'value']
