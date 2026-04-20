from troca.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_new_customer_for_new_user(sender, **kwargs):
    """
    Signal handler that automatically creates a Troca Customer profile
    whenever a new User is registered via the Troca frontend.

    Logic:
        - Listens to the post_save signal of the Custom User model.
        - Checks if the 'created' flag is True (to avoid firing on updates).
        - Filters by 'partner==5' (specific identifier for the Troca tenant/frontend).

    Args:
        sender (Model): The model class (User).
        instance (User): The actual instance being saved.
        created (bool): True if a new record was created.
    """
    if kwargs.get("created"):
        instance = kwargs.get("instance")

        # Partner ID 5 represents the Troca ecosystem context
        if instance.partner == 5:
            Customer.objects.create(user=instance)
