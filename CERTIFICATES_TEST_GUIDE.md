# Quick Test Guide

## Files Modified/Created

1. **conftest.py** (root)
   - Added 17 new fixtures for certificates app
   - All fixtures follow pytest conventions
   - All docstrings and comments in English

2. **certificates/tests.py** (NEW)
   - 39 comprehensive test methods
   - 10 test classes covering different aspects
   - English documentation throughout

## Fixtures Available for Tests

```python
# Staff/User fixtures
staff_user_with_customer()
staff_client()
non_staff_user()
non_staff_client()

# Location fixtures
country_data()
county_data()
town_data()
street_data()
house_data()

# Person/ID fixtures
person_birth_address_data()
id_type_data()
instituition_data()
person_data()
person_list()

# Certificate fixtures
certificate_type_data()
certificate_title_data()
certificate_data()
country_list()
```

## Run Tests

```bash
# All certificates tests
pytest certificates/tests.py -v

# Specific test class
pytest certificates/tests.py::TestCertificateAPI -v

# Specific test
pytest certificates/tests.py::TestCertificateAPI::test_create_certificate -v

# With coverage
pytest certificates/tests.py --cov=certificates

# Show print statements
pytest certificates/tests.py -v -s

# Stop on first failure
pytest certificates/tests.py -x

# Run all tests in project
pytest -v
```

## Test Structure Overview

```
TestCountryAPI
├── test_create_country
├── test_get_countries_list_public
├── test_create_country_authenticated
└── test_country_str_representation

TestPersonAPI
├── test_create_person
├── test_person_full_name
├── test_get_persons_list_staff_only
├── test_create_person_staff_only
├── test_person_str_representation
└── test_person_age_calculation

TestCertificateAPI
├── test_create_certificate
├── test_get_certificates_list_staff_only
├── test_search_certificates_by_person_name
├── test_search_certificates_by_certificate_number
├── test_filter_certificates_by_status
├── test_certificate_number_format
└── test_certificate_str_representation

... (7 more test classes with similar patterns)
```

## Key Testing Features

✅ Staff-only endpoint testing
✅ Non-staff permission denial
✅ Search and filter functionality
✅ Model relationships and hierarchies
✅ Data validation
✅ API status codes validation
✅ Database isolation (pytest marks)
✅ Parametrized test support ready
✅ Fixture-based data setup
✅ Full English documentation

## Integration with Existing Tests

The fixtures in conftest.py are:

- Globally available to all apps
- Can be combined with existing fixtures (staff_client, api_client, etc.)
- Follow Django test best practices
- Compatible with pytest-django

Example combining multiple fixtures:

```python
def test_something(staff_client, certificate_data, person_list):
    # Can use all fixtures together
    pass
```
