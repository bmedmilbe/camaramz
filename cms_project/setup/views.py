from django.shortcuts import render
from .models import UserTokens
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
import requests
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin

import json
from pprint import pprint
# Create your views here.
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import SendEmailResetSerializer, PasswordResetConfirmRetypeSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet

logger = logging.getLogger(__name__)



class PasswordConfirmViewSet(CreateModelMixin, GenericViewSet):
    http_method_name = ['post']
    queryset = UserTokens.objects.all()

    serializer_class = PasswordResetConfirmRetypeSerializer

    # def get_serializer_class(self):
    #     # pprint(self.request.method)
    #     if self.request.method == "POST":
    #         return SendEmailResetSerializer
    #         # if serializer.is_valid():
    #         #     return SendEmailResetSerializer


class PasswordViewSet(CreateModelMixin, GenericViewSet):
    http_method_name = ['post']
    queryset = UserTokens.objects.all()

    serializer_class = SendEmailResetSerializer

    # def get_serializer_class(self):
    #     # pprint(self.request.method)
    #     if self.request.method == "POST":
    #         return SendEmailResetSerializer
    #         # if serializer.is_valid():
    #         #     return SendEmailResetSerializer

    
    # @action(detail=False, methods=["POST"])
    # def email_reset(self, request, *args, **kwargs):
    #     pathner = kwargs.get('pathner', None)
    #     if request.method == "POST":
    #         serializer = SendEmailResetSerializer(data=request.data)
    #         if not serializer.is_valid():
    #             raise serializers.ValidationError({"email": "Email not valid"})
            
    #         serializer.save()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
        
    
                
    # @action(detail=False, methods=["POST"])
    # def email_reset(self, request, *args, **kwargs):
    #     if request.method == "POST":
    #         serializer = SendEmailResetSerializer(data=request.data)
    #         if not serializer.is_valid():
    #             raise serializers.ValidationError({"cart": "This cart is not valid"})
    #         elif not Cart.objects.filter(id=request.data["cart_id"]).exists():
    #             raise serializers.ValidationError({"cart": "This cart does not exists"})

    #         stripe.api_key = settings.STRIPE_SK
    #         cart_id = request.data["cart_id"]
    #         # cart_item = CartItem.objects.get(cart_id= request.kwargs.get('cart_pk'))
    #         # cart = request.data.get('cart')

    #         cart = Cart.objects.get(id=cart_id)

    #         # pprint(cart)

    #         sub_total = settings.PRICE_PARCEL_BY_KG * cart.weigth.quantity

    #         total = round(Decimal((sub_total + Decimal(0.2))) / Decimal(0.975), 2)

    #         tax_list = [0.115 if 1 == "PR" else 0]

    #         fee = (Decimal(total) * Decimal(0.025)) + Decimal(0.2)
    #         # pprint(f"Sub total: {sub_total} Fee: {fee} Total: {total}")

    #         tax = round(sub_total * Decimal(tax_list[0]), 2)

    #         # pprint(f"total: {total}")

    #         # pprint(total)

    #         stripe_total = int(total * 100)
    #         # return 0
    #         intent = stripe.PaymentIntent.create(
    #             amount=stripe_total,
    #             currency="gbp" if cart.country_from.id == 3 else "eur",
    #             automatic_payment_methods={"enabled": True},
    #         )
    #         return Response(
    #             data={"tax": tax, "client_secret": intent.client_secret},
    #             status=status.HTTP_201_CREATED,
    #         )
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    
