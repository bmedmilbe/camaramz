from rest_framework.validators import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from datetime import datetime
from troca.helpers import get_customer
from .models import Customer, Transaction
from rest_framework import serializers
from django.db import transaction


def get_extra_kwargs(fields):
    """
    Utility function to apply a consistent HTML style to serializer fields
    for Browsable API rendering.
    """
    return {
        field: {'style': {'base_template': 'input.html'}}
        for field in fields
        if field not in ['id']
    }


class CustomerSerializer(ModelSerializer):
    """
    Serializer for the Customer model within the financial module.

    Flattens user profile data (first/last name) for easier consumption
    by financial reporting frontends.
    """
    first_name = SerializerMethodField(method_name="get_first_name")
    last_name = SerializerMethodField(method_name="get_last_name")

    class Meta:
        model = Customer
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "boss",
            "is_deliver"
        ]

    def get_first_name(self, customer: Customer):
        """Retrieves first name from the related User model."""
        return customer.user.first_name

    def get_last_name(self, customer: Customer):
        """Retrieves last name from the related User model."""
        return customer.user.last_name


class TransactionSerializer(ModelSerializer):
    """
    Primary serializer for viewing transaction details.

    Provides a comprehensive read-only view of financial settlements,
    including auditing timestamps and agent identification.
    """
    class Meta:
        model = Transaction
        fields = [
            "id",
            "description",
            "value",
            "date",
            "boss",
            "completed",
            "completed_date",
            "completed_by",
            "is_charge",
        ]


class TransactionDeleteSerializer(ModelSerializer):
    """
    Serializer optimized for transaction removal operations.

    Used to ensure that deletion requests are validated against
    business rules (e.g., restricted to specific roles).
    """
    class Meta:
        model = Transaction
        fields = ["id"]


class TransactionCreateSerializer(ModelSerializer):
    """
    Handles the creation logic for new financial transactions.

    Includes business logic to automatically assign the current
    authenticated user as the 'Boss' (Financial Manager) of the record.
    """
    boss_id = serializers.IntegerField(read_only=True)
    completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "description",
            "value",
            "is_charge",
            "completed_by",
            "boss_id",
            "completed",
        ]
        extra_kwargs = get_extra_kwargs(fields=fields)

    def create(self, validated_data):
        """
        Validates the user's authority to create transactions and
        injects the 'boss_id' from the request context.

        Raises:
            ValidationError: If the current user does not have 'Boss' status.
        """
        user = self.context['user']
        customer = get_customer(user)

        if not customer.boss:
            raise ValidationError('You are not boss!')

        validated_data['boss_id'] = customer.id

        return super().create(validated_data)

    def destroy(self, instance, request):
        """
        Ensures that only an authorized Boss can trigger the deletion
        via the serializer context.
        """
        user = self.context['user']
        customer = get_customer(user)

        if not customer.boss:
            raise ValidationError('You are not boss!')
        super().destroy(instance, request)


class TransactionCompleteSerializer(ModelSerializer):
    """
    Handles the finalization (settlement) of a transaction.

    This serializer is used by agents to mark a pending charge/payout
    as completed, capturing the timestamp and responsible agent.
    """
    class Meta:
        model = Transaction
        fields = ["id"]

    def validate(self, attrs):
        """
        Prevents double-settlement by checking the current state.

        Raises:
            ValidationError: If the transaction is already marked as completed.
        """
        if self.instance.completed:
            raise ValidationError('Transaction already completed!')
        return attrs

    def update(self, instance, validated_data):
        """
        Finalizes the transaction by injecting completion metadata
        into the validated data before saving.
        """
        validated_data['completed_by_id'] = self.context['customer_id']
        validated_data['completed'] = True
        validated_data['completed_date'] = datetime.now()

        return super().update(instance, validated_data)
