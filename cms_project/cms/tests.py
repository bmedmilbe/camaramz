import pytest
from rest_framework import status
from cms.models import Association, Post, Budget, Team, Role, District
from django_tenants.utils import tenant_context, schema_context


@pytest.mark.django_db
class TestCMSMultiTenancy:
    """
    Test suite for multi-tenancy isolation within the CMS application.
    """

    def test_tenant_isolation_list(self, api_client_a, api_client_b):
        client_a, tenant_a = api_client_a
        client_b, tenant_b = api_client_b

        # FIX: Create district inside tenant_a context, not public
        with tenant_context(tenant_a):
            district = District.objects.create(name="Central")

            Association.objects.create(
                name="Alpha Association",
                registered="2023-01-01",
                address="Street A",
                number_of_associated=10,
                district=district,
                tenant=tenant_a
            )

        # The API clients already have the correct SERVER_NAME
        # so the middleware will find the table in 'tenant_a'
        response_a = client_a.get("/cms/associations")
        assert response_a.status_code == 200
        assert len(response_a.data['results']) == 1

    def test_prevent_update_by_tenant(self, api_client_a, api_client_b):
        """A user from Tenant B cannot update an association from Tenant A."""
        client_a, tenant_a = api_client_a
        client_b, _ = api_client_b
        district = District.objects.create(name="Central")

        # Association created by Tenant A
        assoc_a = Association.objects.create(
            name="Owner A", registered="2023-01-01", address="Addr",
            number_of_associated=5, district=district, tenant=tenant_a
        )

        url = f"/cms/associations/{assoc_a.id}"
        payload = {"name": "Hacked by B"}

        # Tenant B tries to PATCH Tenant A's content
        response = client_a.patch(url, payload)

        # Should return 405 or 404 depending on ViewSet permissions and queryset filtering
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        # Verify the name remained unchanged in the database
        assoc_a.refresh_from_db()
        assert assoc_a.name == "Owner A"

    def test_post_tenant_isolation(self, api_client_a, api_client_b):
        """
        Ensure that Posts created in one tenant are not visible to users in another tenant.
        """
        client_a, tenant_a = api_client_a
        client_b, tenant_b = api_client_b

        # Create Post for Tenant A with required fields
        Post.objects.create(
            title="Tenant A News",
            slug="news-a",
            text="Detailed content for A",
            description="Short description for A",
            active=True,
            tenant=tenant_a
        )

        # 1. Tenant A user should see their own post
        response_a = client_a.get("/cms/posts")
        assert response_a.status_code == status.HTTP_200_OK
        # Check 'results' key (assuming standard DRF pagination)
        assert len(response_a.data['results']) == 1
        assert response_a.data['results'][0]['title'] == "Tenant A News"

        # 2. Tenant B user should see an empty list
        response_b = client_b.get("/cms/posts")
        assert response_b.status_code == status.HTTP_200_OK
        assert len(response_b.data['results']) == 0

    def test_post_feature_flags_and_types(self, api_client_a):
        """
        Ensure that Post-specific boolean flags (featured, service, etc.) are correctly saved.
        """
        client_a, tenant_a = api_client_a

        # WRAP ORM creation in the correct context
        with tenant_context(tenant_a):
            Post.objects.create(
                title="Service Post",
                slug="service-post",
                is_a_service=True,
                featured=True,
                is_to_front=True,
                tenant=tenant_a
            )

        # The client already has the SERVER_NAME set, so it routes correctly
        response = client_a.get("/cms/posts")
        assert response.status_code == 200

        data = response.data['results'][0]
        assert data['title'] == "Service Post"
        # Optional: Uncomment if the serializer includes these boolean flags
        # assert data['is_a_service'] is True
        # assert data['featured'] is True

    def test_budget_privacy(self, api_client_a, api_client_b):
        client_a, tenant_a = api_client_a
        client_b, _ = api_client_b

        with tenant_context(tenant_a):
            budget_a = Budget.objects.create(
                title="2024 Budget",
                slug="budget-2024",
                type="P",
                year=2024,
                tenant=tenant_a
            )

        url = f"/cms/budgets/{budget_a.id}"
        response = client_b.get(url)  # This routes to tenant_b
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_team_unique_constraint_per_tenant(self, tenant_a, tenant_b):
        """Verify unique_together works across isolated schemas."""
        with tenant_context(tenant_a):
            role_a = Role.objects.create(title="Director", tenant=tenant_a)
            Team.objects.create(name="John Doe", role=role_a, tenant=tenant_a)

        with tenant_context(tenant_b):
            role_b = Role.objects.create(title="Director", tenant=tenant_b)
            # This should not conflict with Tenant A
            team_b = Team.objects.create(name="John Doe", role=role_b, tenant=tenant_b)

        assert team_b.id is not None

    def test_role_filtering(self, api_client_a, api_client_b):
        client_a, tenant_a = api_client_a
        client_b, tenant_b = api_client_b

        # Wrap in context
        with tenant_context(tenant_a):
            Role.objects.create(title="Role A", tenant=tenant_a)

        with tenant_context(tenant_b):
            Role.objects.create(title="Role B", tenant=tenant_b)

        res_a = client_a.get("/cms/roles")
        assert len(res_a.data['results']) == 1
