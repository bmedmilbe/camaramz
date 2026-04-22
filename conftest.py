# conftest.py
import pytest
from rest_framework.test import APIClient
from troca.models import Customer


@pytest.fixture
def api_client():
    """Fixture for a clean API client."""
    return APIClient()


@pytest.fixture
def auth_boss_client(db, django_user_model):
    """Creates an authenticated Boss available for any test in any app."""
    user = django_user_model.objects.create_user(username="boss_admin", password="password")
    customer = Customer.objects.create(user=user, boss=True)

    client = APIClient()
    client.force_authenticate(user=user)
    return client, customer


@pytest.fixture
def deliver_client(db, django_user_model):
    """Creates an authenticated Deliverer available globally."""
    user = django_user_model.objects.create_user(username="deliver_user", password="password")
    customer = Customer.objects.create(user=user, is_deliver=True)

    client = APIClient()
    client.force_authenticate(user=user)
    return client, customer


@pytest.fixture
def deliver_client_2(db, django_user_model):
    """Creates a second authenticated Deliverer available globally."""
    user = django_user_model.objects.create_user(username="deliver_user_2", password="password")
    customer = Customer.objects.create(user=user, is_deliver=True)

    client = APIClient()
    client.force_authenticate(user=user)
    return client, customer
