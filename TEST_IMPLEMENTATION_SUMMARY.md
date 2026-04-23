"""
CERTIFICATES APP TEST IMPLEMENTATION SUMMARY

This document outlines the comprehensive test suite implemented for the certificates app,
following the same pytest-based structure as the troca app.
"""

## TEST STRUCTURE OVERVIEW

### 1. New Fixtures Added to conftest.py

#### Staff User Fixtures:

- `staff_user_with_customer()`: Creates a staff user with backstaff=True
- `staff_client()`: Returns authenticated API client for staff user

#### Non-Staff User Fixtures:

- `non_staff_user()`: Creates regular user without staff privileges
- `non_staff_client()`: Returns authenticated API client for non-staff user

#### Location Model Fixtures:

- `country_data()`: Sample country (Mozambique)
- `county_data()`: Sample county (Mé-Zóchi) with country reference
- `town_data()`: Sample town (Trindade) with county reference
- `street_data()`: Sample street with town reference
- `house_data()`: Sample house with street reference
- `town_data()`: For creating multiple towns

#### Person & Address Fixtures:

- `person_birth_address_data()`: Birth address with country and town
- `id_type_data()`: ID type (BI - Bilhete de Identidade)
- `instituition_data()`: Institution for ID issuance
- `person_data()`: Complete person with all biographical data
- `person_list()`: Multiple persons for list endpoint testing

#### Certificate Model Fixtures:

- `certificate_type_data()`: Certificate type/classification
- `certificate_title_data()`: Certificate variant/title with pricing
- `certificate_data()`: Complete certificate with person reference
- `country_list()`: Multiple countries for list testing

---

## TEST CLASSES & COVERAGE

### TestCountryAPI (4 tests)

- Model creation and validation
- Public list access
- Authenticated user creation
- String representation

### TestPersonAPI (6 tests)

- Person creation with biographical data
- Full name construction
- Staff-only list access (non-staff gets 403)
- Staff-only creation (non-staff gets 403)
- String representation
- Age calculation from birth date

### TestCertificateAPI (7 tests)

- Certificate creation with required fields
- Staff-only list access control
- Search by person name
- Search by certificate number
- Filter by status
- Certificate number format validation (XXX-YYYY)
- String representation

### TestCertificateTitleAPI (3 tests)

- Public access to titles list
- Filter by certificate type
- Price information validation

### TestLocationHierarchy (4 tests)

- Country → County → Town hierarchy
- Street → Town relationship
- House → Street relationship
- Person address relationship

### TestCertificateModelView (2 tests)

- Certificate model endpoint existence
- Metadata endpoint returns all reference data

### TestPermissions (4 tests)

- Staff access to staff endpoints
- Non-staff denied staff endpoints
- Unauthenticated denied staff endpoints
- Public endpoints accessible to all

### TestLocationAPIs (4 tests)

- Counties list endpoint
- Towns list endpoint
- Streets list endpoint
- House creation by authenticated users

### TestPersonBirthAddressAPI (2 tests)

- Birth address creation
- Birth address list access

### TestDataValidation (3 tests)

- Person requires birth_date
- Certificate requires main_person
- Country slug uniqueness

---

## TOTAL TEST COVERAGE

- 39 test methods across 10 test classes
- Covers: Models, API endpoints, Permissions, Validation, Relationships
- Tests both positive (success) and negative (denial) cases

---

## RUNNING THE TESTS

# Run all certificate tests:

pytest certificates/tests.py -v

# Run specific test class:

pytest certificates/tests.py::TestCertificateAPI -v

# Run with coverage:

pytest certificates/tests.py --cov=certificates --cov-report=html

# Run tests for staff permissions only:

pytest certificates/tests.py::TestPermissions -v

---

## KEY TESTING PATTERNS USED (Same as Troca App)

1. **Parametrized Tests**: Not extensively used in this version, can be added for edge cases

2. **Fixture-based Setup**: All test data created via fixtures, no hardcoding

3. **API Endpoint Testing**: Direct HTTP requests using APIClient

4. **Permission Testing**: Explicit tests for staff-only, non-staff, and public endpoints

5. **Status Code Assertions**: Validates both success and error responses

6. **Database Isolation**: Each test runs in isolated database transaction via @pytest.mark.django_db

7. **Relationship Testing**: Validates model relationships and hierarchies

---

## EXAMPLE TEST PATTERNS

### Testing Staff-Only Endpoints:

```python
def test_get_persons_list_staff_only(self, staff_client, non_staff_client, person_list):
    client_staff, _, _ = staff_client
    client_non_staff, _ = non_staff_client
    url = "/api/v1/persons/"

    # Staff user can access
    response = client_staff.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Non-staff user gets denied
    response = client_non_staff.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
```

### Testing Search/Filter:

```python
def test_search_certificates_by_person_name(self, staff_client, certificate_data):
    client_staff, _, _ = staff_client
    url = "/api/v1/certificates/?search=John"

    response = client_staff.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) > 0
```

### Testing Model Validation:

```python
def test_person_requires_birth_date(self, db, person_birth_address_data, ...):
    person = Person(
        name="Test",
        surname="User",
        # birth_date is missing
    )
    with pytest.raises(Exception):
        person.save()
```

---

## FIXTURES REUSABILITY

All fixtures in conftest.py are available globally to:

- certificates app tests
- troca app tests
- Any future app tests

Example usage in other apps:

```python
def test_something(staff_client, person_data, certificate_data):
    # Use any of the globally available fixtures
    pass
```

---

## NEXT STEPS (OPTIONAL ENHANCEMENTS)

1. Add parametrized tests for multiple edge cases:

   ```python
   @pytest.mark.parametrize(
       "gender, expected_suffix",
       [("M", "o"), ("F", "a")],
   )
   def test_person_gender_agreement(self, gender, expected_suffix):
       # Test Portuguese gender agreement
   ```

2. Add integration tests for PDF generation:

   ```python
   def test_pdf_generation_flow(self, staff_client, certificate_data):
       # Test complete PDF generation and storage
   ```

3. Add performance tests:

   ```python
   def test_certificate_list_performance(self, staff_client, django_db_blocker):
       # Test with large dataset
   ```

4. Add API authentication tests:
   ```python
   def test_invalid_token_rejected(self, api_client):
       api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
   ```
