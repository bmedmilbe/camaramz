from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    tenant = models.ForeignKey("Client", on_delete=models.CASCADE, null=True, blank=True)
    valid = models.BooleanField(default=False)
    partner = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = "email"  # Djoser/Django still needs a primary field
    REQUIRED_FIELDS = ["username"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'tenant'],
                name='unique_email_per_tenant',
                condition=models.Q(email__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['phone', 'tenant'],
                name='unique_phone_per_tenant',
                condition=models.Q(phone__isnull=False)
            ),
            models.UniqueConstraint(fields=['username', 'tenant'], name='unique_username_per_tenant')

        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}  {self.email or self.phone} ({self.tenant})"


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=50, unique=True)
    subdomain = models.CharField(max_length=50, unique=True, null=True)

    has_cms = models.BooleanField(default=False)
    contact_email = models.CharField(max_length=100)
    email_password = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=100, null=True)
    logo = models.URLField(null=True)

    def __str__(self):
        return f"{self.name}"


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)

    has_cms = models.BooleanField(default=False)
    contact_email = models.CharField(max_length=100, null=True, blank=True)
    email_password = models.CharField(max_length=100, null=True, blank=True)
    contact_phone = models.CharField(max_length=100, null=True, blank=True)
    logo = models.URLField(null=True, blank=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass


class ClientApp(models.Model):

    APP_CHOICES = [(app, app.split('.')[-1].title()) for app in settings.TENANT_APPS]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_apps")
    app = models.CharField(choices=APP_CHOICES, max_length=100)
    is_active = models.BooleanField(default=True)  # Good for toggling access

    class Meta:
        # Prevent the same app being added twice to the same tenant
        unique_together = ('client', 'app')

    def __str__(self):
        return f"{self.app} - {self.client.name}"
