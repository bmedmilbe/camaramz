from troca.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from pprint import pprint


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_new_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        if kwargs["instance"].partner==5:
            Customer.objects.create(user=kwargs["instance"])

