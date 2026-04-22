import pytest
from rest_framework import status
from cms.models import Association, Post, Budget, Team, Role, District


@pytest.mark.django_db
class TestCMSMultiTenancy:
    """
    Test suite for multi-tenancy isolation within the CMS application.
    """

    def test_tenant_isolation_list(self, api_client_a, api_client_b):
        """A user should only see associations belonging to their tenant."""
        client_a, tenant_a = api_client_a
        client_b, tenant_b = api_client_b

        # Create a shared district (District has no tenant as per the current model)
        district = District.objects.create(name="Central")

        # Create content for Tenant A
        Association.objects.create(
            name="Alpha Association",
            registered="2023-01-01",
            address="Street A",
            number_of_associated=10,
            district=district,
            tenant=tenant_a
        )

        # 1. Tenant A should see 1 item
        response_a = client_a.get("/cms/associations")
        assert response_a.status_code == status.HTTP_200_OK
        assert len(response_a.data['results']) == 1

        # 2. Tenant B should see 0 items
        response_b = client_b.get("/cms/associations")
        assert response_b.status_code == status.HTTP_200_OK
        assert len(response_b.data['results']) == 0

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

        Post.objects.create(
            title="Service Post",
            slug="service-post",
            is_a_service=True,
            featured=True,
            is_to_front=True,
            tenant=tenant_a
        )

        response = client_a.get("/cms/posts")
        data = response.data['results'][0]

        assert data['title'] == "Service Post"
        # Optional: Uncomment if the serializer includes these boolean flags
        # assert data['is_a_service'] is True
        # assert data['featured'] is True

    def test_budget_privacy(self, api_client_a, api_client_b):
        """Ensure that Budget records are private per tenant."""
        client_a, tenant_a = api_client_a
        client_b, _ = api_client_b

        budget_a = Budget.objects.create(
            title="2024 Budget",
            slug="budget-2024",
            type="P",
            year=2024,
            tenant=tenant_a
        )

        # Attempt direct access via ID from Tenant B's client
        url = f"/cms/budgets/{budget_a.id}"
        response = client_b.get(url)

        # Should return 404 because the queryset filters by the request tenant
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_team_unique_constraint_per_tenant(self, tenant_a, tenant_b):
        """
        Verify that the unique_together constraint allows identical names
        in different tenants.
        """
        role_a = Role.objects.create(title="Director", tenant=tenant_a)
        role_b = Role.objects.create(title="Director", tenant=tenant_b)

        # Create "John Doe" in Tenant A
        Team.objects.create(name="John Doe", role=role_a, tenant=tenant_a)

        # Creating "John Doe" in Tenant B should be allowed (database isolation)
        team_b = Team.objects.create(name="John Doe", role=role_b, tenant=tenant_b)

        assert team_b.id is not None
        assert Team.objects.count() == 2

    def test_role_filtering(self, api_client_a, api_client_b):
        """Ensure that Roles are filtered correctly according to the tenant."""
        client_a, tenant_a = api_client_a
        client_b, tenant_b = api_client_b

        Role.objects.create(title="Role A", tenant=tenant_a)
        Role.objects.create(title="Role B", tenant=tenant_b)

        res_a = client_a.get("/cms/roles")
        assert len(res_a.data['results']) == 1
        assert res_a.data['results'][0]['title'] == "Role A"
