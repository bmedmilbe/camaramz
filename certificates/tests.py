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


@pytest.mark.django_db
class TestCountryAPI:
    """Test suite for Country model and API endpoints."""

    def test_create_country(self, country_data):
        """
        Test that a country can be created with required fields.
        """
        assert country_data.name == "Mozambique"
        assert country_data.slug == "mozambique"
        assert country_data.code == 258

    def test_get_countries_not_list_unauthenticated(self, api_client, country_list):
        """
        Test that countries list is not accessible to unauthenticated users only.
        """
        url = "/certificates/countries"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_country_authenticated(self, non_staff_client, country_data):
        """
        Test that authenticated users can create countries.
        """
        client, user = non_staff_client
        url = "/certificates/countries"

        data = {
            "name": "Portugal",
            "slug": "portugal",
            "code": 351
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "Portugal"

    def test_country_str_representation(self, country_data):
        """
        Test that the country string representation is correct.
        """
        assert str(country_data) == "Mozambique"


@pytest.mark.django_db
class TestPersonAPI:
    """Test suite for Person model and API endpoints."""

    def test_create_person(self, person_data):
        """
        Test that a person can be created with biographical information.
        """
        assert person_data.name == "John"
        assert person_data.surname == "Doe"
        assert person_data.gender == "M"
        assert person_data.birth_date == date(1990, 5, 15)

    def test_person_full_name(self, person_data):
        """
        Test that person full name is constructed correctly.
        """
        full_name = f"{person_data.name} {person_data.surname}"
        assert full_name == "John Doe"

    def test_get_persons_list_staff_only(self, staff_client, non_staff_client, person_list):
        """
        Test that persons list is staff-only and non-staff users get 403.
        """
        client_staff, _, _ = staff_client
        client_non_staff, _ = non_staff_client
        url = "/certificates/persons"

        # Staff user can access
        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Non-staff user gets denied
        response = client_non_staff.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_person_staff_only(self, staff_client, non_staff_client,
                                      person_birth_address_data, id_type_data,
                                      instituition_data, house_data):
        """
        Test that creating a person requires staff permissions.
        """
        client_non_staff, _ = non_staff_client
        url = "/certificates/persons"

        data = {
            "name": "Jane",
            "surname": "Smith",
            "gender": "F",
            "birth_date": "1988-04-10",
            "id_number": "111222333",
            "id_type": id_type_data.id,
            "id_issue_date": "2020-01-15",
            "id_issue_local": instituition_data.id,
            "birth_address": person_birth_address_data.id,
            "address": house_data.id,
            "father_name": "John Smith",
            "mother_name": "Mary Smith"
        }

        response = client_non_staff.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_person_str_representation(self, person_data):
        """
        Test that the person string representation is correct.
        """
        expected = "John Doe"
        assert str(person_data) == expected

    def test_person_age_calculation(self, person_data):
        """
        Test that person age can be calculated from birth date.
        """
        today = date.today()
        age = today.year - person_data.birth_date.year
        assert age >= 33  # Born in 1990, so in 2026 would be 35/36


@pytest.mark.django_db
class TestCertificateAPI:
    """Test suite for Certificate model and API endpoints."""

    def test_create_certificate(self, certificate_data):
        """
        Test that a certificate can be created with required data.
        """
        assert certificate_data.main_person.name == "John"
        assert certificate_data.number == "001-2026"
        assert certificate_data.status == "issued"

    def test_get_certificates_list_staff_only(self, staff_client, non_staff_client, certificate_data):
        """
        Test that certificates list requires staff authentication.
        """
        client_staff, _, _ = staff_client
        client_non_staff, _ = non_staff_client
        url = "/certificates/certificates"

        # Staff user can access
        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Non-staff user gets denied
        response = client_non_staff.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_search_certificates_by_person_name(self, staff_client, certificate_data):
        """
        Test that certificates can be searched by person name.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/certificates?search=John"

        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
        assert response.data['results'][0]['main_person']['name'] == "John"

    def test_search_certificates_by_certificate_number(self, staff_client, certificate_data):
        """
        Test that certificates can be searched by certificate number.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/certificates?search=001-2026"

        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_filter_certificates_by_status(self, staff_client, certificate_data):
        """
        Test that certificates can be filtered by status.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/certificates?status=P"

        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_certificate_number_format(self, certificate_data):
        """
        Test that certificate number follows the expected format (XXX-YYYY).
        """
        parts = certificate_data.number.split('-')
        assert len(parts) == 2
        assert parts[0].isdigit()
        assert parts[1].isdigit()

    def test_certificate_str_representation(self, certificate_data):
        """
        Test that the certificate string representation is correct.
        """
        expected = f"Residence Certificate {certificate_data.number}"
        assert str(certificate_data) == expected


@pytest.mark.django_db
class TestCertificateTitleAPI:
    """Test suite for CertificateTitle (variants) API endpoints."""

    def test_deny_non_staff_access(self, api_client, certificate_title_data, non_staff_client):
        """
        Test that certificate titles list is dined for non staff users.
        """
        client_non_staff, _ = non_staff_client
        url = "/certificates/titles"
        response = client_non_staff.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_certificate_titles(self, api_client, certificate_title_data, staff_client):
        """
        Test that certificate titles list for staff users.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/titles"
        response = client_staff.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_filter_certificate_titles_by_type(self, api_client, certificate_title_data, staff_client):
        """
        Test that certificate titles can be filtered by certificate type.
        """
        client_staff, _, _ = staff_client
        cert_type = certificate_title_data.certificate_type
        url = f"/certificates/titles?certificate_type={cert_type.id}"

        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_certificate_title_price(self, certificate_title_data):
        """
        Test that certificate title includes price information.
        """
        assert certificate_title_data.type_price == 50


@pytest.mark.django_db
class TestLocationHierarchy:
    """Test suite for location model relationships and hierarchy."""

    def test_location_hierarchy_country_to_town(self, town_data):
        """
        Test the complete location hierarchy from country to town.
        """
        assert town_data.county is not None
        assert town_data.county.country is not None
        assert town_data.county.country.name == "Mozambique"

    def test_street_belongs_to_town(self, street_data):
        """
        Test that street correctly references its town.
        """
        assert street_data.town is not None
        assert street_data.town.name == "Trindade"

    def test_house_belongs_to_street(self, house_data):
        """
        Test that house correctly references its street.
        """
        assert house_data.street is not None
        assert house_data.street.name == "Main Street"

    def test_person_address_relationship(self, person_data):
        """
        Test that person correctly references their address.
        """
        assert person_data.address is not None
        assert person_data.address.house_number == "123"


@pytest.mark.django_db
class TestCertificateModelView:
    """Test suite for dynamic serializer selection in CertificateModelViewSet."""

    def test_certificate_model_endpoint_exists(self, staff_client, certificate_title_data):
        """
        Test that the certificate model creation endpoint is accessible.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_data.id}/model"

        response = client_staff.get(url)
        assert response.status_code in [status.HTTP_405_METHOD_NOT_ALLOWED]

    def test_metadata_endpoint_returns_all_reference_data(self, staff_client):
        """
        Test that the metadata endpoint returns all reference data in one call.
        """

        client_staff, _, _ = staff_client
        url = "/certificates/metadata"
        response = client_staff.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Check that response contains expected keys
        expected_keys = [
            'countries', 'universities', 'ifens', 'buildings',
            'cemiterios', 'streets', 'changes', 'towns', 'countys',
            'certificateTitles', 'covals', 'idtypes', 'intituitions'
        ]
        for key in expected_keys:
            assert key in response.data


@pytest.mark.django_db
class TestPermissions:
    """Test suite for certificate app permissions."""

    def test_staff_user_can_access_person_endpoints(self, staff_client):
        """
        Test that staff users can access staff-only endpoints.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/persons"

        response = client_staff.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_non_staff_user_denied_person_endpoints(self, non_staff_client):
        """
        Test that non-staff users are denied access to staff-only endpoints.
        """
        client_non_staff, _ = non_staff_client
        url = "/certificates/persons"

        response = client_non_staff.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_denied_staff_endpoints(self, api_client):
        """
        Test that unauthenticated users are denied access to staff-only endpoints.
        """
        url = "/certificates/persons"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_public_endpoints_unaccessible_to_all(self, api_client, country_data):
        """
        Test that public endpoints are accessible to unauthenticated users.
        """
        url = "/certificates/countries"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLocationAPIs:
    """Test suite for location-related API endpoints."""

    def test_get_counties_list(self, api_client, county_data, staff_client):
        """
        Test that counties list endpoint is accessible.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/countys"
        response = client_staff.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_towns_list(self, api_client, town_data, staff_client):
        """
        Test that towns list endpoint is accessible.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/towns"
        response = client_staff.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_streets_list(self, api_client, street_data, staff_client):
        """
        Test that streets list endpoint is accessible.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/streets"
        response = client_staff.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_create_house_by_staff(self, staff_client, street_data):
        """
        Test that authenticated users can create house addresses.
        """
        client_staff, _, _ = staff_client
        url = "/certificates/house"

        data = {
            "street": street_data.id,
            "house_number": "456"
        }

        response = client_staff.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPersonBirthAddressAPI:
    """Test suite for PersonBirthAddress API endpoints."""

    def test_create_birth_address(self, non_staff_client, country_data, town_data):
        """
        Test that birth address can be created with valid data.
        """
        client, user = non_staff_client
        url = "/certificates/birthadddress"

        data = {
            "birth_country": country_data.id,
            "town": town_data.id
        }

        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_birth_addresses_list(self, api_client, person_birth_address_data):
        """
        Test that birth addresses list is accessible.
        """
        url = "/certificates/birthadddress"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDataValidation:
    """Test suite for data validation in models."""

    def test_person_requires_birth_date(db, person_birth_address_data,
                                        id_type_data, instituition_data, house_data):
        data = {
            "name": "Test",
            "surname": "User",
            "gender": "M",
            "id_number": "123456",
            "id_type": id_type_data.id,
            "id_issue_date": date.today(),
            "id_issue_local": instituition_data.id,
            "birth_address": person_birth_address_data.id,
            "address": house_data.id,
            "father_name": "Father",  # Added to pass your parent check
            # "birth_date" is missing
        }

        serializer = PersonCreateOrUpdateSerializer(data=data)

        # This will now RAISE a ValidationError because of the extra_kwargs
        assert serializer.is_valid() is False
        assert 'birth_date' in serializer.errors

    def test_certificate_requires_main_person(self, db, certificate_title_data):
        """
        Test that certificate requires a main_person.
        """
        certificate = Certificate(
            # main_person is missing
            type=certificate_title_data,
            number="TEST-2026",
            date_issue=date.today()
        )

        # Use django.core.exceptions.ValidationError for specific testing
        from django.core.exceptions import ValidationError

        with pytest.raises(ValidationError) as excinfo:
            certificate.full_clean()

        # Optional: verify the error is on the correct field
        assert 'main_person' in excinfo.value.message_dict

    def test_country_name_uniqueness(self, db, country_data):
        """
        Test that country name must be unique.
        """
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            Country.objects.create(
                name="Mozambique",  # Same name as country_data
                slug="mozambique",  # Same slug as country_data
                code=999
            )


@pytest.mark.django_db
class TestCertificateCreationNestedRoute:
    """
    Test suite for creating different certificate types using the nested route.

    The nested route structure is: POST /certificates/titles/{title_pk}/model/
    This endpoint dynamically selects serializers based on certificate type.
    """

    def test_create_certificate_type_one(self, staff_client, certificate_title_type_one,
                                         person_data, person_secondary_data, house_data):
        """
        Test creation of Type One certificate (basic attestation).
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_one.id}/model"
        print(url)
        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
        }

        response = client_staff.post(url, data, format='json')

        # If it fails, this will show you the exact validation error
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Validation Errors: {response.data}")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['secondary_person'] == person_secondary_data.id

    def test_create_certificate_fails_missing_data(self, staff_client, certificate_title_type_one):
        """
        Ensure that the request fails with 400 Bad Request if mandatory fields are missing.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_one.id}/model"

        # Sending empty data to trigger validation error
        response = client_staff.post(url, {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_certificate_type_two(self, staff_client, certificate_title_type_two,
                                         person_data, person_secondary_data, house_data,
                                         instituition_data, university_data):
        """
        Test creation of Type Two certificate (education related).
        Uses CertificateModelTwoCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_two.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
            "instituition": instituition_data.id,
            "university": university_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['instituition'] == instituition_data.id
        assert response.data['university'] == university_data.id

    def test_create_certificate_type_three(self, staff_client, certificate_title_type_three,
                                           person_data, person_secondary_data, house_data):
        """
        Test creation of Type Three certificate (date related).
        Uses CertificateModelThreeCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_three.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
            "date": date.today().isoformat(),
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['secondary_person'] == person_secondary_data.id

    def test_create_certificate_type_fifth(self, staff_client, certificate_title_type_fifth,
                                           person_data, person_secondary_data, house_data,
                                           instituition_data):
        """
        Test creation of Type Fifth certificate (institution related).
        Uses CertificateModelFifthCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_fifth.id}/model"
        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
            "instituition": instituition_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        # If it fails, this will show you the exact validation error
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Validation Errors: {response.data}")
        assert response.data['main_person'] == person_data.id
        if 'instituition' in response.data:
            assert response.data['instituition'] == instituition_data.id

    def test_create_certificate_type_enterro(self, staff_client, certificate_title_type_enterro,
                                             person_data, person_secondary_data, cemiterio_data,
                                             available_grave, deceased_person_details):
        """
        Test creation of Type Enterro certificate (burial).
        Verifies plot recycling logic: closing an old grave and creating a new one.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_enterro.id}/model"

        # Define dates
        died_dt = date.today() - timedelta(days=1)
        burial_dt = date.today()

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "cemiterio": cemiterio_data.id,
            "died_date": died_dt.isoformat(),
            "entero_date": burial_dt.isoformat(),
        }

        response = client_staff.post(url, data, format='json')

        # 1. Assert Response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id

        # 2. Assert Side Effect: Grave Recycling
        from certificates.models import Coval

        # Verify the old grave is now closed
        available_grave.refresh_from_db()
        assert available_grave.closed is True

        # Verify a new grave record was created for the deceased
        new_grave = Coval.objects.filter(
            name=deceased_person_details.name,
            date_of_deth=died_dt
        ).first()

        assert new_grave is not None
        assert new_grave.cemiterio == cemiterio_data
        assert new_grave.square == available_grave.square
        # Verify numbering format (count + 1 - year square)
        assert f"-{date.today().year}" in new_grave.number

    def test_create_certificate_type_coval(self, staff_client, certificate_title_type_coval,
                                           person_data, person_secondary_data, coval_data):
        """
        Test creation of Type CovalCompra certificate (burial plot purchase).
        Uses CertificateModelCertCompraCovalCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_coval.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "coval": coval_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['coval'] == coval_data.id

    def test_create_certificate_type_auto_mod_coval(self, staff_client,
                                                    certificate_title_type_auto_mod_coval,
                                                    person_data, person_secondary_data,
                                                    coval_data, change_data):
        """
        Test creation of Type AutoModCoval certificate (burial plot modification).
        Uses CertificateModelAutoModCovalCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_auto_mod_coval.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "coval": coval_data.id,
            "change": change_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['coval'] == coval_data.id
        assert response.data['change'] == change_data.id

    def test_create_certificate_type_barraca(self, staff_client, range_data, certificate_title_type_barraca,
                                             person_data, person_secondary_data, street_data):
        """
        Test creation of Type LicBarraca certificate (market stall license).
        Uses CertificateModelLicBarracaCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_barraca.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "street": street_data.id,
            "object": "Market Stall",
            "range": range_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['street'] == street_data.id

    def test_create_certificate_type_construcao(self, staff_client,
                                                certificate_title_type_construcao,
                                                person_data, person_secondary_data,
                                                building_type_data, street_data):
        """
        Test creation of Type AutoConstrucao certificate (construction authorization).
        Uses CertificateModelAutoConstrucaoCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_construcao.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "building_type": building_type_data.id,
            "street": street_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['building_type'] == building_type_data.id
        assert response.data['street'] == street_data.id

    def test_create_certificate_type_seventh(self, staff_client, certificate_title_type_seventh,
                                             person_data, person_secondary_data, house_data,
                                             country_data):
        """
        Test creation of Type Seventh certificate (country/duration related).
        Uses CertificateModelSeventhCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_seventh.id}/model"
        print(url)
        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
            "years": 5,
            "country": country_data.id,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['country'] == country_data.id

    def test_create_certificate_type_buffet(self, staff_client, certificate_title_type_buffet,
                                            person_data, person_secondary_data, street_data):
        """
        Test creation of Type LicencaBuffet certificate (catering license).
        Uses CertificateModelLicencaBuffetCreateSerializer.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_buffet.id}/model"
        print(url)
        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "street": street_data.id,
            "infra": "Restaurant",
            "metros": 50,
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['main_person'] == person_data.id
        assert response.data['street'] == street_data.id

    def test_create_certificate_without_staff_permission(self, non_staff_client,
                                                         certificate_title_type_one,
                                                         person_data, person_secondary_data,
                                                         house_data):
        """
        Test that non-staff users cannot create certificates via nested route.
        """
        client_non_staff, _ = non_staff_client
        url = f"/certificates/titles/{certificate_title_type_one.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
        }

        response = client_non_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_certificate_unauthenticated(self, api_client, certificate_title_type_one,
                                                person_data, person_secondary_data,
                                                house_data):
        """
        Test that unauthenticated users cannot create certificates via nested route.
        """
        url = f"/certificates/titles/{certificate_title_type_one.id}/model"

        data = {
            "main_person": person_data.id,
            "secondary_person": person_secondary_data.id,
            "house": house_data.id,
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_certificate_with_missing_required_fields(self, staff_client,
                                                             certificate_title_type_one):
        """
        Test that certificate creation fails with missing required fields.
        """
        client_staff, _, _ = staff_client
        url = f"/certificates/titles/{certificate_title_type_one.id}/model"

        data = {
            # Missing main_person, secondary_person, and house
        }

        response = client_staff.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
