import pytest
from rest_framework import status
from rest_framework.test import APIClient
from troca.models import Customer, Transaction
from datetime import timezone


@pytest.mark.django_db
class TestTransactionCreation:

    @pytest.mark.parametrize(
        "value, description, is_charge, expected_status",
        [
            (100, "Valid transaction", True, status.HTTP_201_CREATED),
            (0, "Zero value", True, status.HTTP_400_BAD_REQUEST),
            (-50, "Negative value", False, status.HTTP_400_BAD_REQUEST),
            (200, "", False, status.HTTP_400_BAD_REQUEST),  # Empty description
        ],
    )
    def test_add_transaction_logic(self, auth_boss_client, value, description, is_charge, expected_status):
        """
        Test the POST /troca/transactions/ endpoint.
        """
        api_client, boss_customer = auth_boss_client
        url = "/troca/transactions/"

        data = {
            "value": value,
            "description": description,
            "is_charge": is_charge
        }

        # Use format='json' to ensure the payload is correctly sent
        response = api_client.post(url, data, format='json')

        assert response.status_code == expected_status

    def test_non_boss_cannot_create_transaction(self, django_user_model):
        """
        Ensures that a user without boss=True receives a 400 error from the serializer.
        """
        api_client = APIClient()
        user = django_user_model.objects.create_user(username="regular_user", password="password")
        Customer.objects.create(user=user, boss=False)  # Not a boss
        api_client.force_authenticate(user=user)

        data = {"value": 100, "description": "Attempt", "is_charge": True}
        response = api_client.post("/troca/transactions/", data, format='json')

        # The serializer raises ValidationError('You are not boss!') which results in 400
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "You are not boss!" in str(response.data)


@pytest.mark.django_db
class TestTransactionBusinessLogic:

    def test_complete_transaction_success(self, auth_boss_client, deliver_client):
        """Tests if a deliverer can complete an open transaction."""
        api_boss, boss = auth_boss_client
        api_deliver, deliver = deliver_client

        # 1. Boss creates a transaction

        transaction = Transaction.objects.create(
            description="Fast delivery",
            value=50,
            boss=boss,
            is_charge=False,
            completed_by=deliver
        )

        # 2. Deliverer attempts to complete it
        url = f"/troca/transactions/{transaction.id}/complete/"

        response = api_deliver.patch(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['completed'] is True

        # Verify in database
        transaction.refresh_from_db()
        assert transaction.completed is True
        assert transaction.completed_by == deliver

    def test_transaction_not_found(self, auth_boss_client, deliver_client, deliver_client_2):
        """Tests if a deliverer can complete an open transaction."""
        api_boss, boss = auth_boss_client
        api_deliver, deliver = deliver_client
        api_deliver_2, deliver_2 = deliver_client_2

        # 1. Boss creates a transaction

        transaction = Transaction.objects.create(
            description="Fast delivery",
            value=50,
            boss=boss,
            is_charge=False,
            completed_by=deliver_2  # Assigning to a different deliverer to simulate not found for current deliver
        )

        # 2. Deliverer attempts to complete it
        url = f"/troca/transactions/{transaction.id}/complete/"

        response = api_deliver.patch(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_complete_already_completed_transaction(self, auth_boss_client, deliver_client):
        """Ensures that a transaction cannot be completed twice."""
        api_boss, boss = auth_boss_client
        api_deliver, deliver = deliver_client

        transaction = Transaction.objects.create(
            description="Already done",
            value=50,
            boss=boss,
            completed=True,  # Already finalized
            completed_by=deliver
        )

        url = f"/troca/transactions/{transaction.id}/complete/"
        response = api_deliver.patch(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Transaction already completed!" in str(response.data)

    def test_balance_calculation(self, auth_boss_client, deliver_client):
        """Tests if the balance calculation correctly sums entries and exits."""
        api_boss, boss = auth_boss_client
        _, deliver = deliver_client

        # Create completed transactions
        # Entry (Charge)
        Transaction.objects.create(boss=boss, completed_by=deliver, value=100, is_charge=True, completed=True)
        # Exit (Payment)
        Transaction.objects.create(boss=boss, completed_by=deliver, value=30, is_charge=False, completed=True)

        url = "/troca/transactions/balance/"
        response = api_boss.get(url, {"boss": boss.id, "deliver": deliver.id})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['enter'] == 100
        assert response.data['out'] == 30

    def test_delete_transaction_permission(self, auth_boss_client, deliver_client):
        """Only the Boss who owns the transaction can delete it."""
        api_boss, boss = auth_boss_client
        api_deliver, _ = deliver_client

        transaction = Transaction.objects.create(description="Delete me", value=10, boss=boss)

        # 1. Deliverer tries to delete (Should fail)
        url = f"/troca/transactions/{transaction.id}/"
        response_fail = api_deliver.delete(url)

        # Note: Your ViewSet uses IsBoss for the custom 'delete' action
        # But for the standard ModelViewSet DELETE, it checks IsAuthenticated
        # If using the custom action /delete/:
        url_custom = f"/troca/transactions/{transaction.id}/delete/"
        response_fail = api_deliver.post(url_custom)  # Assuming it's POST or DELETE as configured

        assert response_fail.status_code == status.HTTP_403_FORBIDDEN

    def test_queryset_privacy(self, auth_boss_client, django_user_model):
        """Ensures a Boss cannot see transactions from other users."""
        # Create another Boss
        api_boss_3 = APIClient()
        user_3 = django_user_model.objects.create_user(username="boss_3", password="p")
        Customer.objects.create(user=user_3, boss=True)
        api_boss_3.force_authenticate(user=user_3)

        # Create another Boss
        user_2 = django_user_model.objects.create_user(username="boss2", password="p")
        boss_2 = Customer.objects.create(user=user_2, boss=True)

        # Transaction belonging to Boss 2
        Transaction.objects.create(description="Invisible", value=50, boss=boss_2)

        # Boss 1 tries to list transactions
        response = api_boss_3.get("/troca/transactions/")

        assert response.status_code == status.HTTP_200_OK
        # The result should be empty since boss_1 is not involved in boss_2's transaction
        assert len(response.data['results']) == 0
