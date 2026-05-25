
from rest_framework.validators import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from troca.helpers import get_customer
from .models import Customer, Transaction
from rest_framework import serializers
from django.db import transaction


def get_extra_kwargs(fields):
    return {
        field: {'style': {'base_template': 'input.html'}}
        for field in fields
        if field not in ['id']
    }


class CustomerSerializer(ModelSerializer):
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
        return customer.user.first_name

    def get_last_name(self, customer: Customer):
        return customer.user.last_name


class TransactionSerializer(ModelSerializer):

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

    class Meta:
        model = Transaction
        fields = [
            "id",

        ]

    def delete(self, instance):

        return instance.delete()


class TransactionCreateSerializer(ModelSerializer):
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
        user = self.context['user']
        customer = get_customer(user)

        if not customer.boss:
            raise ValidationError('You are not boss!')

        validated_data['boss_id'] = customer.id

        return super().create(validated_data)

    def destroy(self, instance, request):
        user = self.context['user']
        customer = get_customer(user)

        if not customer.boss:
            raise ValidationError('You are not boss!')
        super().destroy(instance, request)


class TransactionCompleteSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id"]

    def validate(self, attrs):
        if self.instance.completed:
            raise ValidationError('Transaction already completed!')
        return attrs

    def update(self, instance, validated_data):
        validated_data['completed_by_id'] = self.context['customer_id']
        validated_data['completed'] = True
        validated_data['completed_date'] = timezone.now()

        return super().update(instance, validated_data)
