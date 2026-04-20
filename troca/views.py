from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework import status
from django.db import transaction, DatabaseError
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from rest_framework.decorators import action
from .helpers import get_boss, get_customer
from .models import Customer, Transaction
from .serializers import (
    CustomerSerializer,
    TransactionCreateSerializer,
    TransactionDeleteSerializer,
    TransactionSerializer,
    TransactionCompleteSerializer,
)


class IsBoss(BasePermission):
    """
    Custom permission to only allow users identified as a 'Boss' (Financial Manager)
    to perform specific administrative actions.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return get_boss(user)
        return False


class CustomerViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for viewing customer profiles involved in financial exchanges.

    Provides 'me' action to retrieve the authenticated user's financial profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """Scopes the queryset to optimized customers ordered by name."""
        return Customer.objects.optimized().all().order_by("user__first_name")

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retrieves the financial customer profile of the logged-in user."""
        customer = get_customer(request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class TransactionViewSet(ModelViewSet):
    """
    The Core engine for financial settlements in the 'Troca' module.

    Implements multi-tenant scoped transactions, pessimistic locking for
    concurrency control, and complex balance aggregations.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['boss', 'completed_by', 'is_charge', 'completed']
    search_fields = ['id', 'description']

    def get_serializer_class(self):
        """Returns specific serializers based on the request action."""
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_queryset(self):
        """
        Retrieves transactions filtered by the user's role (Boss or Deliverer).
        Ensures data isolation between financial agents.
        """
        user = self.request.user
        boss = get_boss(user)
        customer = get_customer(user)

        return Transaction.objects.optimized().filter(
            Q(boss=boss) | Q(completed_by=customer)
        ).distinct()

    def create(self, request, *args, **kwargs):
        """
        Initiates a new financial transaction.
        Scoping is automatically handled by the serializer context.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """
        Marks a transaction as completed using Pessimistic Locking.

        Uses select_for_update to lock the row during the atomic block,
        preventing race conditions during financial settlement.
        """
        with transaction.atomic():
            # Lock the specific transaction row until the end of this block
            transaction_obj = get_object_or_404(
                self.get_queryset().select_for_update(of=('self',), nowait=True),
                pk=pk
            )
            serializer = TransactionCompleteSerializer(
                transaction_obj,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(TransactionSerializer(transaction_obj).data)

    @action(detail=False, methods=['get'], permission_classes=[IsBoss])
    def history(self, request):
        """Retrieves a historical log of all transactions managed by the Boss."""
        boss = get_boss(request.user)
        transactions = Transaction.objects.optimized().filter(boss=boss)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(data={'results': serializer.data})

    @action(detail=True, methods=['delete'], permission_classes=[IsBoss])
    def delete(self, request, pk=None):
        """
        Safely deletes a transaction record using atomic locking.
        Only accessible by the Financial Manager (Boss).
        """
        with transaction.atomic():
            transaction_obj = get_object_or_404(
                self.get_queryset().select_for_update(of=('self',), nowait=True),
                pk=pk,
                boss__user=self.request.user
            )
            serializer = TransactionDeleteSerializer(
                transaction_obj,
                data=request.data or {},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            transaction_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def balance(self, request, pk=None):
        """
        Calculates and returns the aggregated financial balance.

        Returns:
            dict: A dictionary containing the sum of entries ('enter')
                  and exits ('out') for a specific agent/boss pair.
        """
        boss_id = request.query_params.get("boss")
        deliver_id = request.query_params.get("deliver")

        # Aggregate total entries (charges)
        enter = Transaction.objects.optimized().filter(
            completed_by_id=deliver_id,
            boss_id=boss_id,
            is_charge=True
        ).aggregate(enter=Sum("value"))

        # Aggregate total completed exits
        out = Transaction.objects.optimized().filter(
            completed_by_id=deliver_id,
            boss_id=boss_id,
            completed=True,
            is_charge=False
        ).aggregate(out=Sum("value"))

        return Response(enter | out)
