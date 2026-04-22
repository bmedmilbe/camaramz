"""Helper functions for the certificates application.

Provides utility functions for customer management, time calculations,
and status mapping.
"""

from certificates.classes.interfaces.document import Document
from django.conf import settings
from .models import Customer
from datetime import datetime
from pprint import pprint
import re


def get_customer(user: settings.AUTH_USER_MODEL):
    """Retrieve the Customer object associated with a user.

    Args:
        user: Django user instance (settings.AUTH_USER_MODEL).

    Returns:
        Customer: The Customer object associated with the user, or None if not found.

    Example:
        >>> customer = get_customer(request.user)
        >>> if customer:
        ...     print(f"Customer level: {customer.level}")
    """
    return Customer.objects.filter(user_id=user.id).first()


def get_user(customer: Customer):
    """Retrieve the User object associated with a Customer.

    Args:
        customer: Customer instance.

    Returns:
        settings.AUTH_USER_MODEL: The user object linked to the customer, or None if not found.

    Example:
        >>> user = get_user(customer)
    """
    return settings.AUTH_USER_MODEL.objects.filter(customer_set_id=customer.id).first()


def caculate_time(obj_date: datetime):
    """Calculate human-readable time difference from given date to now.

    Calculates elapsed time and returns a formatted string like "2 hours ago"
    or "3 days ago". Falls back to the datetime object if difference is >= 1 year.

    Args:
        obj_date: datetime object to compare against current time.

    Returns:
        str or datetime: Human-readable time difference (e.g., "2 hours ago") or
                        the original datetime if >= 1 year has passed.

    Example:
        >>> time_diff = caculate_time(some_datetime)
        >>> print(time_diff)  # Output: "3 days ago"
    """
    time = datetime.now()
    if obj_date.day == time.day:
        return str(time.hour - obj_date.hour) + " hours ago"
    elif obj_date.month == time.month:
        return str(time.day - obj_date.day) + " days ago"
    elif obj_date.year == time.year:
        return str(time.month - obj_date.month) + " months ago"

    return obj_date


def shipping_status(status):
    """Map shipping status code to human-readable status label.

    Converts single-character status codes to descriptive status names
    for display purposes.

    Args:
        status: Single character status code (P/M/O/C/R).
            - "P": Finding a deliver
            - "M": Collecting
            - "O": On the way
            - "C": Completed
            - "R": Refunded/Returned

    Returns:
        str: Human-readable status label, or None if status code not recognized.

    Example:
        >>> label = shipping_status("C")
        >>> print(label)  # Output: "Completed"
    """
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
