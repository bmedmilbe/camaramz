from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import connection
from django.apps import apps  # Import apps helper
from django_tenants.utils import schema_context
from certificates.models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_new_customer_for_new_user(sender, instance, created, **kwargs):
    if not created:
        return

    current_schema = connection.get_schema()

    # Safety: don't run this in the public schema
    if current_schema == 'public':
        return

    # Get the model dynamically by string
    ClientApp = apps.get_model('core', 'ClientApp')

    with schema_context('public'):
        has_certificate_app = ClientApp.objects.filter(
            client__schema_name=current_schema,
            app='certificates',
            is_active=True
        ).exists()

    if has_certificate_app:
        Customer.objects.get_or_create(user=instance)
