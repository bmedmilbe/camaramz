"""Signal handlers for the certificates application.

Registers Django signal handlers for automatic model creation and cleanup.
"""

from certificates.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_new_customer_for_new_user(sender, instance, created, **kwargs):
    """Signal handler to create a Customer when a new user is created.

    Automatically creates a Customer record for users created under tenant id=2.
    This ensures that users created in specific tenants have corresponding
    Customer records with default staff level and status.

    Args:
        sender: The model class that sent the signal (settings.AUTH_USER_MODEL).
        instance: The actual instance of the user being saved.
        created: Boolean indicating whether the user was newly created (True) or updated (False).
        **kwargs: Additional keyword arguments from Django signals.

    Returns:
        None

    Note:
        Only creates Customer records for users with tenant_id=2.
        Uses get_or_create to prevent duplicate Customer records.

    Example:
        >>> # This handler is automatically triggered when:
        >>> new_user = User.objects.create(username='john', tenant_id=2)
        >>> # Customer is automatically created with backstaff=False, level=1
    """
    if not created:
        return

    # Create a Customer for users created under tenant id=2
    if getattr(instance, "tenant_id", None) == 2:
        Customer.objects.get_or_create(user=instance)
