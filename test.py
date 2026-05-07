"""
Test suite for the certificates app.

Tests cover:
- Model creation and validation
- API endpoint access and permissions
- Certificate generation and management
- Staff-only operations
- Filtering, searching, and ordering functionality
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta
from certificates.models import (
    Certificate, Country, County, Person, PersonBirthAddress,
    CertificateTitle, CertificateTypes, House, Street, Town,
    IDType, Instituition, Parent, Ifen, BiuldingType, Cemiterio, Coval, Change
)
from certificates.serializers import PersonCreateOrUpdateSerializer
from django_tenants.utils import tenant_context


@pytest.mark.django_db
class TestPersonAPI:

    def test_create_person(self, tenant_a, person_data):
        # FIX: person_data has a relation to Country.
        # Accessing person_data requires the schema context.
        with tenant_context(tenant_a):
            assert person_data.name == "John"
            assert person_data.gender == "M"

    def test_person_full_name(self, tenant_a, person_data):
        with tenant_context(tenant_a):
            full_name = f"{person_data.name} {person_data.surname}"
            assert full_name == "John Doe"

    def test_get_persons_list_permissions(self, staff_client, non_staff_client):
        # The fixtures now handle SERVER_NAME, so no context needed here for the API call
        client_staff, _, _ = staff_client
        client_non_staff, _ = non_staff_client
        url = "/certificates/persons"
        assert client_staff.get(url).status_code == status.HTTP_200_OK
        assert client_non_staff.get(url).status_code == status.HTTP_403_FORBIDDEN

    def test_create_person_staff_only(self, tenant_a, non_staff_client, id_type_data, house_data):
        client_non_staff, _ = non_staff_client
        url = "/certificates/persons"
        # FIX: accessing id_type_data.id triggers a query to 'certificates_idtype'
        with tenant_context(tenant_a):
            data = {
                "name": "Jane",
                "id_type": id_type_data.id,
                "address": house_data.id,
            }
        response = client_non_staff.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_person_detail_isolation(self, api_client_b, person_data):
        """Tenant B should not find Tenant A's person."""
        client_b, tenant_b = api_client_b
        # person_data is in Tenant A. client_b points to Tenant B.
        url = f"/certificates/persons/{person_data.id}/"
        response = client_b.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
