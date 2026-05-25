
from certificates.models import Cemiterio, CertificateRange, Coval, Change, Country, County
from datetime import date
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import Tenant
from troca.models import Customer
from certificates.models import CertificateSimplePerson, Customer as CertificateCustomer

from datetime import date, timedelta
# conftest.py additions
from django_tenants.utils import tenant_context, schema_context
from core.models import Client, Domain  # Import your new Client model

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture for a clean API client."""
    return APIClient()


@pytest.fixture(scope='session', autouse=True)
def setup_public_tenant(django_db_setup, django_db_blocker):
    """Essential: django-tenants needs a public schema to function."""
    with django_db_blocker.unblock():
        client, _ = Client.objects.get_or_create(
            schema_name='public',
            defaults={'name': 'Public'}
        )
        Domain.objects.get_or_create(
            domain='testserver',  # Default for APIClient
            tenant=client,
            is_primary=True
        )


@pytest.fixture
def auth_boss_client(db, django_user_model, tenant_a):
    """Authenticated client using unique email to avoid IntegrityError."""
    with tenant_context(tenant_a):
        user = django_user_model.objects.create_user(
            username="boss_admin",
            password="password",
            email="boss_admin@test.com",  # Add unique email
            tenant=tenant_a
        )
        from troca.models import Customer
        customer = Customer.objects.create(user=user, boss=True)

    client = APIClient()
    client.defaults['SERVER_NAME'] = 'tenant-a.testserver'
    client.force_authenticate(user=user)
    return client, customer


@pytest.fixture
def deliver_client(db, django_user_model, tenant_a):
    with tenant_context(tenant_a):
        user = django_user_model.objects.create_user(
            username="deliver_user",
            password="password",
            email="deliver_1@test.com",  # Add unique email
            tenant=tenant_a
        )
        customer = Customer.objects.create(user=user, is_deliver=True)
    client = APIClient()
    client.defaults['SERVER_NAME'] = 'tenant-a.testserver'
    client.force_authenticate(user=user)
    return client, customer


@pytest.fixture
def deliver_client_2(db, django_user_model, tenant_a):  # Add tenant_a
    with tenant_context(tenant_a):
        user = django_user_model.objects.create_user(
            username="deliver_user_2",
            password="password",
            tenant=tenant_a
        )
        customer = Customer.objects.create(user=user, is_deliver=True)

    client = APIClient()
    client.defaults['SERVER_NAME'] = 'tenant-a.testserver'
    client.force_authenticate(user=user)
    return client, customer

# CMS App fixtures


@pytest.fixture
def tenant_a(db, django_db_blocker):
    """
    Creates a tenant, its domain, and initializes the tenant schema with migrations.
    """
    from django.core.management import call_command
    from django.db import connection

    with django_db_blocker.unblock():
        with schema_context('public'):
            tenant, created = Client.objects.get_or_create(
                schema_name='tenant_a',
                defaults={'name': 'Tenant A'}
            )
            Domain.objects.get_or_create(
                domain='tenant-a.testserver',
                tenant=tenant,
                is_primary=True
            )

            # Ensure the schema exists and run migrations in it.
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {tenant.schema_name}')

            with schema_context(tenant.schema_name):
                call_command('migrate', verbosity=0, interactive=False)

    return tenant


@pytest.fixture
def tenant_b(db, django_db_blocker):
    """
    Creates a tenant, its domain, and initializes the tenant schema with migrations.
    """
    from django.core.management import call_command
    from django.db import connection

    with django_db_blocker.unblock():
        with schema_context('public'):
            tenant, created = Client.objects.get_or_create(
                schema_name='tenant_b',
                defaults={'name': 'Tenant B'}
            )
            Domain.objects.get_or_create(
                domain='tenant-b.testserver',
                tenant=tenant,
                is_primary=True
            )

            # Ensure the schema exists and run migrations in it.
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {tenant.schema_name}')

            with schema_context(tenant.schema_name):
                call_command('migrate', verbosity=0, interactive=False)

    return tenant


@pytest.fixture
def api_client_a(tenant_a):
    from django_tenants.utils import tenant_context
    with tenant_context(tenant_a):
        user, _ = User.objects.get_or_create(
            username="user_a_cms",
            defaults={
                "email": "user_a_cms@test.com",
                "phone": "123456789",
                "tenant": tenant_a
            }
        )
        user.set_password("password")
        user.save()

    client = APIClient()
    # Set the domain so the middleware routes to tenant_a
    client.defaults['SERVER_NAME'] = 'tenant-a.testserver'
    client.force_authenticate(user=user)
    return client, tenant_a


@pytest.fixture
def api_client_b(tenant_b, django_user_model):
    from django_tenants.utils import tenant_context
    with tenant_context(tenant_b):
        user = django_user_model.objects.create_user(
            username="user_b_cms",
            password="password",
            email="user_b_cms@test.com",
            tenant=tenant_b
        )
    client = APIClient()
    # Set the domain so the middleware routes to tenant_b
    client.defaults['SERVER_NAME'] = 'tenant-b.testserver'
    client.force_authenticate(user=user)
    return client, tenant_b


@pytest.fixture
def admin_user_with_tenant(db, tenant_a):
    """
    Creates a superuser that satisfies your User manager requirements.
    """
    from django_tenants.utils import tenant_context
    with tenant_context(tenant_a):
        return User.objects.create_superuser(
            username="admin_test",
            email="admin @ test.com",
            password="password",
            phone="999999999",  # Add this if your manager requires it
            tenant=tenant_a     # Superusers usually need a default tenant too
        )


# Certificates App Fixtures

@pytest.fixture(autouse=True)
def setup_essential_metadata(db, tenant_a):
    """Wrap all setup logic in the tenant context."""
    from django_tenants.utils import tenant_context

    with tenant_context(tenant_a):
        # Move all your existing logic here
        from django.utils import timezone
        from certificates.models import (
            Ifen, CertificateTypes, CertificateTitle,
            Parent, CertificateSinglePerson, CertificateSimpleParent
        )

        # 1. Setup Ifen records (required for document rendering)
        Ifen.objects.get_or_create(name="data", defaults={"size": 1000})
        Ifen.objects.get_or_create(name="texto", defaults={"size": 1000})

        # 2. Setup CertificateType (Base type)
        cert_type_base, _ = CertificateTypes.objects.get_or_create(
            name="Standard Type"
        )

        # 3. Setup CertificateTitle (ID 12 is critical for FifthSerializer logic)
        title_12, _ = CertificateTitle.objects.get_or_create(
            id=12,
            defaults={
                "name": "General Purpose Certificate",
                "certificate_type": cert_type_base,
                "type_price": 100.00,
                "slug": "generic-cert-12",
                "goal": "Testing"
            }
        )

        # 4. Setup Parent record (Required for CertificateSimpleParent)
        parent_obj, _ = Parent.objects.get_or_create(
            title="Father",
            defaults={
                "in_plural": "Fathers",
                "in_plural_mix": "Parents",
                "degree": 1,
                "gender": "M"
            }
        )

        # 5. Add CertificateSinglePerson (Satisfies count() check in FifthSerializer)
        CertificateSinglePerson.objects.get_or_create(
            type=title_12,
            name="Default Single Person",
            defaults={"gender": "M"}
        )

        # 6. Add CertificateSimpleParent (Satisfies count() check in FifthSerializer)
        # Note: Use the model name correctly as defined in your models.py
        sp = CertificateSimpleParent.objects.get_or_create(
            type=title_12,
            name="Default Child",
            defaults={
                "birth_date": timezone.now().date(),
                "parent": parent_obj
            }
        )
        # 7. Setup CertificateSimplePerson (The one you just added)
        # Satisfies the: CertificateSimplePerson.objects.filter(type_id=12).count() check
        CertificateSimplePerson.objects.update_or_create(
            type=title_12,
            name="Default Simple Person",
            defaults={
                "gender": "M",
                "birth_date": timezone.now().date()
            }
        )


@pytest.fixture
def range_data(db, tenant_a):
    """
    Creates sample certificate range data.
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateRange
        # Using update_or_create to prevent IntegrityErrors if run multiple times
        cert_range, _ = CertificateRange.objects.update_or_create(
            type="C",  # Matches TYPE_ADVENCED
            defaults={
                "price": 100.00,
            }
        )
    return cert_range


@pytest.fixture
def staff_user_with_customer(db, tenant_a):
    from django_tenants.utils import tenant_context
    with tenant_context(tenant_a):
        user, _ = User.objects.get_or_create(
            username="staff_user",
            defaults={
                "password": "password",
                "email": "staff@test.com",
                "phone": "111111111",
                "tenant": tenant_a
            }
        )
        # Use update_or_create to handle existing customers
        customer, _ = CertificateCustomer.objects.update_or_create(
            user=user,
            defaults={"backstaff": True}
        )
    return user, customer


@pytest.fixture
def non_staff_user(db, tenant_a):
    """Creates a regular user inside the tenant schema."""
    from django_tenants.utils import tenant_context
    with tenant_context(tenant_a):
        user = User.objects.create_user(
            username="regular_user",
            password="password",
            email="user@test.com",
            phone="222222222",
            tenant=tenant_a
        )
        CertificateCustomer.objects.create(user=user, backstaff=False)
    return user


@pytest.fixture
def staff_client(staff_user_with_customer, tenant_a):
    user, customer = staff_user_with_customer
    client = APIClient()

    # 1. This tells the Middleware to route requests to the tenant_a schema
    client.defaults['SERVER_NAME'] = 'tenant-a.testserver'

    # 2. Wrap authentication in context so it can find the 'Customer' table
    with tenant_context(tenant_a):
        client.force_authenticate(user=user)
        return client, user, customer


@pytest.fixture
def non_staff_client(non_staff_user, tenant_a):
    client = APIClient()
    client.defaults['SERVER_NAME'] = 'tenant-a.testserver'
    with tenant_context(tenant_a):
        client.force_authenticate(user=non_staff_user)
        return client, non_staff_user


@pytest.fixture
def town_data(db, county_data, tenant_a):
    """
    Creates sample town/municipality data.
    """
    with tenant_context(tenant_a):
        from certificates.models import Town
        town = Town.objects.create(
            name="Trindade",
            slug="trindade",
            county=county_data
        )
    return town


@pytest.fixture
def street_data(db, town_data, tenant_a):
    """
    Creates sample street data.
    """
    with tenant_context(tenant_a):
        from certificates.models import Street
        street = Street.objects.create(
            name="Main Street",
            slug="main-street",
            town=town_data
        )
    return street


@pytest.fixture
def house_data(db, street_data, tenant_a):
    """
    Creates sample house/address data.
    """
    with tenant_context(tenant_a):
        from certificates.models import House
        house = House.objects.create(
            street=street_data,
            house_number="123"
        )
    return house


@pytest.fixture
def person_birth_address_data(db, country_data, town_data, tenant_a):
    """
    Creates sample birth address data for a person.
    """
    with tenant_context(tenant_a):
        from certificates.models import PersonBirthAddress
        birth_address = PersonBirthAddress.objects.create(
            birth_country=country_data,
            birth_town=town_data
        )
    return birth_address


@pytest.fixture
def id_type_data(db, tenant_a):
    """
    Creates sample ID type data.
    """
    with tenant_context(tenant_a):
        from certificates.models import IDType
        id_type = IDType.objects.create(
            name="Bilhete de Identidade",
        )
    return id_type


@pytest.fixture
def instituition_data(db, tenant_a):
    """
    Creates sample institution data.
    """
    with tenant_context(tenant_a):
        from certificates.models import Instituition
        institution = Instituition.objects.create(
            name="Test Institution",
        )
    return institution


@pytest.fixture
def person_data(db, person_birth_address_data, id_type_data, instituition_data, house_data, tenant_a):
    """
    Creates sample person (individual) data with biographical information.
    """
    with tenant_context(tenant_a):
        from certificates.models import Person
        person = Person.objects.create(
            name="John",
            surname="Doe",
            gender="M",
            birth_date=date(1990, 5, 15),
            id_number="123456789",
            id_type=id_type_data,
            id_issue_date=date(2015, 1, 1),
            id_issue_local=instituition_data,
            birth_address=person_birth_address_data,
            address=house_data,
            father_name="James Doe",
            mother_name="Jane Doe"
        )
    return person


@pytest.fixture
def certificate_type_data(db, tenant_a):
    """
    Creates sample certificate type (classification) data.
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTypes
        cert_type = CertificateTypes.objects.create(
            name="Attestation",
            slug="attestation"
        )
    return cert_type


@pytest.fixture
def certificate_title_data(db, certificate_type_data, tenant_a):
    """
    Creates sample certificate title (variant) data.
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title = CertificateTitle.objects.create(
            id=45,
            name="Residence Certificate",
            slug="residence-certificate",
            certificate_type=certificate_type_data,
            type_price=50
        )
    return cert_title


@pytest.fixture
def certificate_data(db, person_data, certificate_title_data, tenant_a):
    """
    Creates sample certificate data for testing.
    """
    with tenant_context(tenant_a):
        from certificates.models import Certificate
        certificate = Certificate.objects.create(
            main_person=person_data,
            type=certificate_title_data,
            number="001-2026",
            date_issue=date.today(),
            status="issued"
        )
    return certificate


@pytest.fixture
def country_list(db, tenant_a):
    """
    Creates multiple countries for testing list endpoints.
    """
    with tenant_context(tenant_a):
        from certificates.models import Country
        countries = [
            Country.objects.create(name="Angola", slug="angola", code=244),
            Country.objects.create(name="Cape Verde", slug="cape-verde", code=238),
            Country.objects.create(name="Guinea-Bissau", slug="guinea-bissau", code=245),
        ]
    return countries


@pytest.fixture
def person_list(db, person_birth_address_data, id_type_data, instituition_data, house_data, tenant_a):
    """
    Creates multiple persons for testing list endpoints.
    """
    with tenant_context(tenant_a):
        from certificates.models import Person
        persons = [
            Person.objects.create(
                name="Alice",
                surname="Smith",
                gender="F",
                birth_date=date(1995, 3, 20),
                id_number="987654321",
                id_type=id_type_data,
                id_issue_date=date(2018, 6, 15),
                id_issue_local=instituition_data,
                birth_address=person_birth_address_data,
                address=house_data,
                father_name="Robert Smith",
                mother_name="Mary Smith"
            ),
            Person.objects.create(
                name="Bob",
                surname="Johnson",
                gender="M",
                birth_date=date(1992, 7, 10),
                id_number="555666777",
                id_type=id_type_data,
                id_issue_date=date(2016, 2, 1),
                id_issue_local=instituition_data,
                birth_address=person_birth_address_data,
                address=house_data,
                father_name="William Johnson",
                mother_name="Patricia Johnson"
            ),
        ]
    return persons


# Additional Fixtures for Certificate Creation Tests

@pytest.fixture
def person_secondary_data(db, person_birth_address_data, id_type_data, instituition_data, house_data, tenant_a):
    """
    Creates a secondary person for certificates that require two people.
    """
    with tenant_context(tenant_a):
        from certificates.models import Person
        person = Person.objects.create(
            name="Jane",
            surname="Smith",
            gender="F",
            birth_date=date(1988, 4, 10),
            id_number="111222333",
            id_type=id_type_data,
            id_issue_date=date(2020, 1, 15),
            id_issue_local=instituition_data,
            birth_address=person_birth_address_data,
            address=house_data,
            father_name="John Smith",
            mother_name="Mary Smith"
        )
    return person


@pytest.fixture
def university_data(db, tenant_a):
    """
    Creates sample university data for certificate creation.
    """
    with tenant_context(tenant_a):
        from certificates.models import University
        university = University.objects.create(
            name="University of Test"
        )
    return university


@pytest.fixture
def country_data(db, tenant_a):
    """Creates a sample country."""
    with tenant_context(tenant_a):
        country, _ = Country.objects.get_or_create(
            name="Mozambique",
            defaults={"slug": "mozambique", "code": 258}
        )
    return country


@pytest.fixture
def county_data(db, country_data, tenant_a):
    """Creates a sample county linked to a country."""
    with tenant_context(tenant_a):
        county, _ = County.objects.get_or_create(
            name="Mé-Zóchi",
            defaults={"slug": "me-zochi", "country": country_data}
        )
    return county


@pytest.fixture
def cemiterio_data(db, county_data, tenant_a):
    """
    Fixed Fixture: Creates a cemetery with the required county_id.
    Uses update_or_create to prevent ID conflicts.
    """
    with tenant_context(tenant_a):
        from certificates.models import Cemiterio
        cemiterio, _ = Cemiterio.objects.update_or_create(
            id=1,
            defaults={
                "name": "Central Cemetery",
                "county": county_data  # This provides the missing county_id
            }
        )
    return cemiterio


@pytest.fixture
def coval_data(db, cemiterio_data, tenant_a):
    """
    Creates sample burial plot (coval) data.
    """
    with tenant_context(tenant_a):
        from certificates.models import Coval
        coval = Coval.objects.create(
            nick_number="CV001",
            number="001",
            square="A",
            name="Test Plot",
            date_used=date.today(),
            cemiterio=cemiterio_data,
            date_of_deth=date.today() - timedelta(days=2),  # Ensure this is not None
        )
    return coval


@pytest.fixture
def change_data(db, tenant_a):
    """
    Creates sample change (modification type) data.
    """
    with tenant_context(tenant_a):
        from certificates.models import Change
        change = Change.objects.create(
            name="Ownership Change",
            price=25.50
        )
    return change


@pytest.fixture
def building_type_data(db, tenant_a):
    """
    Creates sample building type data.
    """
    with tenant_context(tenant_a):
        from certificates.models import BiuldingType
        building_type = BiuldingType.objects.create(
            name="Commercial Building",
            prefix="Bld"
        )
    return building_type


@pytest.fixture
def parent_data(db, tenant_a):
    """
    Creates sample parent/relative data.
    """
    with tenant_context(tenant_a):
        from certificates.models import Parent
        parent = Parent.objects.create(
            title="Son",
            in_plural="Sons",
            in_plural_mix="Sons and Daughters",
            degree=1,
            gender="M"
        )
    return parent


@pytest.fixture
def certificate_type_one(db, tenant_a):
    """
    Creates certificate type for basic certificates (Type One).
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTypes
        cert_type, _ = CertificateTypes.objects.get_or_create(
            slug="attestation",
            defaults={
                "name": "Attestation",
                "gender": "o"
            }
        )
    return cert_type


@pytest.fixture
def certificate_type_enterro(db, tenant_a):
    """
    Creates certificate type for burial/enterro certificates.
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTypes
        cert_type, _ = CertificateTypes.objects.get_or_create(
            slug="burial-certificate",
            defaults={
                "name": "Burial Certificate",
                "gender": "o"
            }
        )
    return cert_type


@pytest.fixture
def certificate_type_licenca(db, tenant_a):
    """
    Creates certificate type for license certificates.
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTypes
        cert_type, _ = CertificateTypes.objects.get_or_create(
            slug="license",
            defaults={
                "name": "License",
                "gender": "a"
            }
        )
    return cert_type


@pytest.fixture
def certificate_title_type_one(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type One (basic attestation).
    ID: 1 (maps to CertificateModelOneCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=1,
            defaults={
                "name": "Basic Attestation",
                "slug": "basic-attestation",
                "certificate_type": certificate_type_one,
                "type_price": 50
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_two(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type Two (education related).
    ID: 3 (maps to CertificateModelTwoCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=3,
            defaults={
                "name": "Education Certificate",
                "slug": "education-certificate",
                "certificate_type": certificate_type_one,
                "type_price": 60,
                "goal": "educational"
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_three(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type Three (date related).
    ID: 2 (maps to CertificateModelThreeCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=2,
            defaults={
                "name": "Date Certificate",
                "slug": "date-certificate",
                "certificate_type": certificate_type_one,
                "type_price": 55
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_fifth(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type Fifth (institution related).
    ID: 12 (maps to CertificateModelFifthCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.get_or_create(
            id=12,
            defaults={
                "name": "General Purpose Certificate",
                "certificate_type": certificate_type_one,
                "type_price": 100.00,
                "slug": "generic-cert-12",
                "goal": "Testing"
            }
        )
    return cert_title


@pytest.fixture
def change_data(db, tenant_a):
    """Creates a sample modification type (Change)."""
    with tenant_context(tenant_a):
        return Change.objects.create(
            name="Marble Headstone Installation",
            price=150.00
        )


@pytest.fixture
def country_data(db, tenant_a):
    """Creates a sample country."""
    with tenant_context(tenant_a):
        country, _ = Country.objects.get_or_create(
            name="Mozambique",
            defaults={"slug": "mozambique", "code": 258}
        )
    return country


@pytest.fixture
def county_data(db, country_data, tenant_a):
    """Creates a sample county linked to a country."""
    with tenant_context(tenant_a):
        county, _ = County.objects.get_or_create(
            name="Mé-Zóchi",
            defaults={"slug": "me-zochi", "country": country_data}
        )
    return county


@pytest.fixture
def cemiterio_data(db, county_data, tenant_a):
    """
    Fixed Fixture: Creates a cemetery with the required county_id.
    Uses update_or_create to prevent ID conflicts.
    """
    with tenant_context(tenant_a):
        from certificates.models import Cemiterio
        cemiterio, _ = Cemiterio.objects.update_or_create(
            id=1,
            defaults={
                "name": "Central Cemetery",
                "county": county_data  # This provides the missing county_id
            }
        )
    return cemiterio


@pytest.fixture
def certificate_title_type_enterro(db, certificate_type_enterro, tenant_a):
    """
    Creates a certificate title for Type Enterro (burial).
    ID: 33 (maps to CertificateModelEnterroCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=33,
            defaults={
                "name": "Burial Certificate",
                "slug": "burial-certificate",
                "certificate_type": certificate_type_enterro,
                "type_price": 100
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_coval(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type CovalCompra (burial plot purchase).
    ID: 24 (maps to CertificateModelCertCompraCovalCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=24,
            defaults={
                "name": "Plot Purchase Certificate",
                "slug": "plot-purchase-certificate",
                "certificate_type": certificate_type_one,
                "type_price": 75
            }
        )
    return cert_title


@pytest.fixture
def available_grave(db, cemiterio_data, tenant_a):
    """
    Creates an 'old' grave record that satisfies the recycling logic
    (date_used < today - 1 year AND closed=False).
    """
    with tenant_context(tenant_a):
        from certificates.models import Coval
        from datetime import date
        return Coval.objects.create(
            number="1-OLD",
            nick_number="PLOT-001",
            square="A",
            date_used=date(2000, 1, 1),  # Very old grave
            closed=False,
            cemiterio=cemiterio_data
        )


@pytest.fixture
def deceased_person_details(db, certificate_title_type_enterro, tenant_a):
    """
    The serializer requires a record in CertificateSinglePerson
    linked to the type_id (Enterro) to provide the deceased's name/gender.
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateSinglePerson
        return CertificateSinglePerson.objects.create(
            type_id=certificate_title_type_enterro.id,
            name="John Doe Deceased",
            gender="M"
        )


@pytest.fixture
def certificate_title_type_auto_mod_coval(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type AutoModCoval (burial plot modification).
    ID: 25 (maps to CertificateModelAutoModCovalCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=25,
            defaults={
                "name": "Plot Modification Certificate",
                "slug": "plot-modification-certificate",
                "certificate_type": certificate_type_one,
                "type_price": 80
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_barraca(db, certificate_type_licenca, tenant_a):
    """
    Creates a certificate title for Type LicBarraca (market stall license).
    ID: 27 (maps to CertificateModelLicBarracaCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=27,
            defaults={
                "name": "Market Stall License",
                "slug": "market-stall-license",
                "certificate_type": certificate_type_licenca,
                "type_price": 85
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_construcao(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type AutoConstrucao (construction authorization).
    ID: 23 (maps to CertificateModelAutoConstrucaoCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=23,
            defaults={
                "name": "Construction Authorization",
                "slug": "construction-authorization",
                "certificate_type": certificate_type_one,
                "type_price": 70
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_seventh(db, certificate_type_one, tenant_a):
    """
    Creates a certificate title for Type Seventh (country/duration related).
    ID: 18 (maps to CertificateModelSeventhCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=18,
            defaults={
                "name": "Residence Duration Certificate",
                "slug": "residence-duration-certificate",
                "certificate_type": certificate_type_one,
                "type_price": 90
            }
        )
    return cert_title


@pytest.fixture
def certificate_title_type_buffet(db, certificate_type_licenca, tenant_a):
    """
    Creates a certificate title for Type LicencaBuffet (catering license).
    ID: 29 (maps to CertificateModelLicencaBuffetCreateSerializer)
    """
    with tenant_context(tenant_a):
        from certificates.models import CertificateTitle
        cert_title, _ = CertificateTitle.objects.update_or_create(
            id=29,
            defaults={
                "name": "Catering License",
                "slug": "catering-license",
                "certificate_type": certificate_type_licenca,
                "type_price": 95
            }
        )
    return cert_title
