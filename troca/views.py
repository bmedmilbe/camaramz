from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from pprint import pprint
from django.db.models import Q, Sum
from .helpers import get_boss, get_customer
from .serializers import (
    CustomerSerializer,
    TransactionCreateSerializer,
    TransactionDeleteSerializer,
    TransactionSerializer,
    TransactionCompleteSerializer,
    TransactionUncompleteSerializer,
    TransactionChargeSerializer

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

        transaction = self.get_object()
        serializer = TransactionCompleteSerializer(data=request.data, context=context)

        transaction = serializer.update(transaction, request.data)
        pprint(transaction.completed)
        return Response(TransactionCreateSerializer(transaction).data)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete(self, request, pk=None):
        customer = get_customer(self.request.user)
        context = {'customer_id': customer.id, 'boss': customer.boss}

        transaction = self.get_object()
        serializer = TransactionDeleteSerializer(data=request.data, context=context)
        transaction = serializer.delete(transaction)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def uncomplete(self, request, pk=None):
        customer = get_customer(self.request.user)
        context = {'customer_id': customer.id}

        transaction = self.get_object()
        serializer = TransactionUncompleteSerializer(data=request.data, context=context)
        transaction = serializer.update(transaction, request.data)
        return Response(TransactionSerializer(transaction).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def total_i_charged(self, request, pk=None):
        customer = get_customer(self.request.user)
        deliver_id = request.query_params.get("deliver")
        charges = Transaction.objects.optimized().filter(Q(deliver_id=deliver_id), Q(boss=customer),
                                                         is_charge=True).aggregate(total=Sum("value"))
        # pprint(charges)
        # serializer = ChargeSerializer(charges, many=True)
        return Response(charges)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def total_i_got(self, request, pk=None):
        customer = get_customer(self.request.user)
        boss_id = request.query_params.get("boss")
        charges = Transaction.objects.optimized().filter(Q(completed_by=customer), Q(boss_id=boss_id),
                                                         is_charge=True).aggregate(total=Sum("value"))
        # pprint(charges)
        # serializer = ChargeSerializer(charges, many=True)
        return Response(charges)

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def total_i_delivered(self, request, pk=None):
        customer = get_customer(self.request.user)
        boss_id = request.query_params.get("boss")
        total = Transaction.objects.optimized().filter(Q(completed_by=customer), Q(boss_id=boss_id),
                                                       is_charge=False, completed=True).aggregate(total=Sum("value"))
        # pprint(charges)
        # serializer = ChargeSerializer(charges, many=True)
        return Response(total)
