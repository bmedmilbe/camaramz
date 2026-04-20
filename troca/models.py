from django.conf import settings
from django.db import models


class CustomerQuerySet(models.QuerySet):
    """
    Custom QuerySet for Customer model to centralize database optimizations.
    """

    def optimized(self):
        """
        Uses select_related to perform a SQL JOIN with the User table,
        reducing database hits when accessing user profile data.
        """
        return self.select_related("user")


class Customer(models.Model):
    """
    Financial profile linked to a User. Defines roles within the 'Troca' system.

    Attributes:
        boss (bool): If True, the user acts as a Financial Manager/Administrator.
        is_deliver (bool): If True, the user acts as an agent executing transactions.
    """
    objects = CustomerQuerySet.as_manager()
    boss = models.BooleanField(default=False)
    is_deliver = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="troca_customer"
    )

    def __str__(self):
        return self.user.first_name


class TransactionQuerySet(models.QuerySet):
    """
    Custom QuerySet for Transactions to handle complex relationship fetching.
    """

    def optimized(self):
        """
        Optimizes fetching by joining both the Manager (boss) and
        the executing Agent (completed_by) details in a single query.
        """
        return self.select_related("boss__user", "completed_by__user")


class Transaction(models.Model):
    """
    Represents a financial settlement or exchange record.

    This model is the core of the remittance system, tracking values,
    responsible parties, and completion status.
    """
    objects = TransactionQuerySet.as_manager()
    description = models.CharField(max_length=255)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    # The Manager responsible for authorizing the transaction
    boss = models.ForeignKey(
        Customer,
        related_name="boss_transactions",
        on_delete=models.PROTECT
    )

    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    # The Agent who physically executed or closed the transaction
    completed_by = models.ForeignKey(
        Customer,
        related_name="deliver_transactions",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    # Distinguishes between a debt/charge and a standard transaction
    is_charge = models.BooleanField(default=False)
