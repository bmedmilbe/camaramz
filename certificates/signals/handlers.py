from certificates.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_new_customer_for_new_user(sender, instance, created, **kwargs):
    if not created:
        return

    # Create a Customer for users created under tenant id=2
    if getattr(instance, "tenant_id", None) == 2:
        Customer.objects.get_or_create(user=instance)

