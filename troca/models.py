from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class CustomerQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related("user")


class Customer(models.Model):
    objects = CustomerQuerySet.as_manager()
    boss = models.BooleanField(default=False)
    is_deliver = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="troca_customer")

    def __str__(self):
        return self.user.first_name


class TransactionQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related("boss__user", "completed_by__user")


class Transaction(models.Model):
    objects = TransactionQuerySet.as_manager()
    description = models.CharField(max_length=255)
    value = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateTimeField(auto_now_add=True)

    boss = models.ForeignKey(Customer, related_name="boss_transactions", on_delete=models.PROTECT)

    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(Customer, related_name="deliver_transactions",
                                     on_delete=models.PROTECT, null=True, blank=True)

    is_charge = models.BooleanField(default=False)
