from pprint import pprint

from django.conf import settings
from .models import Customer


def get_customer(user: settings.AUTH_USER_MODEL):
    # pprint(list(Customer.objects.all()))
    return user.troca_customer


def get_boss(user: settings.AUTH_USER_MODEL):
    return user.troca_customer.boss


def get_user(customer: Customer):
    return settings.AUTH_USER_MODEL.objects.optimized().filter(customer_set_id=customer.id).first()
