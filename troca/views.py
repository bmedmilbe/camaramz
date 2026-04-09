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
from pprint import pprint
from django.db.models import Q, Sum
from .helpers import get_boss, get_customer
from .serializers import (
    CustomerSerializer,
    TransactionCreateSerializer,
    TransactionDeleteSerializer,
    TransactionSerializer,
    TransactionCompleteSerializer,

)
from rest_framework.decorators import action
from .models import Customer, Transaction

# Create your views here.


class IsBoss(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return get_boss(user)
        return False


class CustomerViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.optimized().all().order_by("user__first_name")

    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = get_customer(request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class TransactionViewSet(ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.optimized().filter(Q(boss__user=user) | Q(completed_by__user=user)).order_by('-id')

    def get_serializer_class(self):
        # pprint(self.request.method)
        if self.request.method in ['POST', 'PATCH']:
            return TransactionCreateSerializer

        return TransactionSerializer

    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter,
                       DjangoFilterBackend, OrderingFilter]

    filterset_fields = ['boss', 'is_charge', 'completed', 'completed_by']
    search_fields = ['description', 'value']

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        customer = get_customer(self.request.user)
        context = {'customer_id': customer.id}

        try:
            with transaction.atomic():
                transaction_obj = get_object_or_404(
                    self.get_queryset().select_for_update(of=('self',), nowait=True), pk=pk)
                serializer = TransactionCompleteSerializer(transaction_obj,
                                                           data=request.data,
                                                           context=context,
                                                           partial=True)
                serializer.is_valid(raise_exception=True)
                updated_transaction = serializer.save()
            return Response(TransactionCreateSerializer(updated_transaction).data)
        except DatabaseError:
            return Response(
                {"detail": "This transaction is currently being processed by another user. Please try again in a moment."},
                status=status.HTTP_409_CONFLICT
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def previews(self, request):
        max_id = int(request.query_params.get("max_id", 0))
        boss_id = int(request.query_params.get("boss", 0))
        completed_by_id = int(request.query_params.get("completed_by", 0))
        limit = int(request.query_params.get("limit", 10))

        if max_id <= 0:
            transactions = Transaction.objects.optimized().filter(
                Q(boss_id=boss_id), Q(completed_by_id=completed_by_id)).order_by('-id')[:limit]
        else:
            transactions = Transaction.objects.optimized().filter(
                Q(boss_id=boss_id), Q(completed_by_id=completed_by_id), id__lt=max_id).order_by('-id')[:limit]

        serializer = TransactionSerializer(transactions, many=True)
        return Response(data={'results': serializer.data})

    @action(detail=True, methods=['delete'], permission_classes=[IsBoss])
    def delete(self, request, pk=None):
        with transaction.atomic():
            transaction_obj = get_object_or_404(
                self.get_queryset().select_for_update(of=('self',), nowait=True),
                pk=pk,
                boss__user=self.request.user)
            serializer = TransactionDeleteSerializer(transaction_obj,
                                                     data=request.data or {},
                                                     context={'request': request})
            serializer.is_valid(raise_exception=True)
            transaction_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def balance(self, request, pk=None):
        boss_id = request.query_params.get("boss")
        deliver_id = request.query_params.get("deliver")
        enter = Transaction.objects.optimized().filter(
            completed_by_id=deliver_id,
            boss_id=boss_id,
            is_charge=True).aggregate(
            enter=Sum("value"))
        out = Transaction.objects.optimized().filter(
            completed_by_id=deliver_id,
            boss_id=boss_id,
            completed=True,
            is_charge=False).aggregate(
            out=Sum("value"))

        return Response(enter | out)
