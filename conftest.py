
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import Tenant
from troca.models import Customer


User = get_user_model()


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


# CMS App fixtures

@pytest.fixture
def tenant_a(db):
    # Use get_or_create to avoid IntegrityError (unique name constraint)
    tenant, _ = Tenant.objects.get_or_create(name="Tenant A", domain="a.com", subdomain="a.a.com")
    return tenant


@pytest.fixture
def tenant_b(db):
    tenant, _ = Tenant.objects.get_or_create(name="Tenant B", domain="b.com", subdomain="b.b.com")
    return tenant


@pytest.fixture
def api_client_a(tenant_a):
    # Create user with all required fields (added phone/email if necessary)
    user, _ = User.objects.get_or_create(
        username="user_a",
        defaults={
            "email": "user_a@test.com",
            "phone": "123456789",
            "tenant": tenant_a
        }
    )
    user.set_password("password")
    user.save()

    client = APIClient()
    client.force_authenticate(user=user)
    client.credentials(HTTP_X_TENANT_ID=str(tenant_a.id))
    return client, tenant_a


@pytest.fixture
def api_client_b(tenant_b, django_user_model):
    user = django_user_model.objects.create_user(username="user_b", password="password", tenant=tenant_b)
    client = APIClient()
    client.force_authenticate(user=user)
    client.credentials(HTTP_X_TENANT_ID=str(tenant_b.id))
    return client, tenant_b


@pytest.fixture
def admin_user_with_tenant(db, tenant_a):
    """
    Creates a superuser that satisfies your User manager requirements.
    """
    return User.objects.create_superuser(
        username="admin_test",
        email="admin@test.com",
        password="password",
        phone="999999999",  # Add this if your manager requires it
        tenant=tenant_a     # Superusers usually need a default tenant too
    )
