from certificates.classes.interfaces.document import Document
from django.conf import settings
from .models import Customer
from datetime import datetime
from pprint import pprint
import re

def get_customer(user: settings.AUTH_USER_MODEL):
    # pprint(list(Customer.objects.all()))
    return Customer.objects.filter(user_id=user.id).first()


def get_user(customer: Customer):
    return settings.AUTH_USER_MODEL.objects.filter(customer_set_id=customer.id).first()


def caculate_time(obj_date: datetime):
    # pprint(order.deliverorder.first().deliver.customer.user.first_name)
    # return f'{order.created_at|timesince}'
    # pprint(obj_date)
    time = datetime.now()
    if obj_date.day == time.day:
        return str(time.hour - obj_date.hour) + " hours ago"
    elif obj_date.month == time.month:
        return str(time.day - obj_date.day) + " days ago"
    elif obj_date.year == time.year:
        return str(time.month - obj_date.month) + " months ago"

    return obj_date


def shipping_status(status):
    # pprint(order.deliverorder.first().deliver.customer.user.first_name)
    # return f'{order.created_at|timesince}'
    SHIPPING_STATUS_FINDING_DELIVER = "P"
    SHIPPING_STATUS_DELIVER_COLLECTING = "M"
    SHIPPING_STATUS_ONTHEWAY = "O"
    SHIPPING_STATUS_DELIVER_COMPLETED = "C"
    SHIPPING_STATUS_RETURNED = "R"
    SHIPPING_STATUS_CHOICES = [
        (SHIPPING_STATUS_DELIVER_COLLECTING, "Collecting"),
        (SHIPPING_STATUS_DELIVER_COMPLETED, "Completed"),
        (SHIPPING_STATUS_FINDING_DELIVER, "Findig a deliver"),
        (SHIPPING_STATUS_RETURNED, "Refunded"),
        (SHIPPING_STATUS_ONTHEWAY, "On the way"),
    ]

    for shipping_status in SHIPPING_STATUS_CHOICES:
        if shipping_status[0] == status:
            return shipping_status[1]

    return "Unknown"


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s
