from django.conf import settings
from .models import Customer


def get_customer(user: settings.AUTH_USER_MODEL):
    """
    Retrieves the Troca Customer profile associated with a standard User.
    Used primarily in Middleware and Viewsets for context binding.
    """
    return user.troca_customer


def get_boss(user: settings.AUTH_USER_MODEL):
    """
    Checks if the given user has administrative (Boss) privileges
    within the financial module.
    """
    return user.troca_customer.boss


def get_user(customer: Customer):
    """
    Reverse lookup to find the Auth User model from a Customer instance.
    Uses optimized filtering to retrieve the user object.
    """
    return settings.AUTH_USER_MODEL.objects.optimized().filter(
        customer_set_id=customer.id
    ).first()
