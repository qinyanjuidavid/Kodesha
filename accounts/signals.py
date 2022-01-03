from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import (Administrator, Buyer, Seller, User)


@receiver(post_save, sender=User)
def create_users(sender, instance, created, **kwargs):
    if created:
        if(instance.is_admin or instance.is_staff):
            Administrator.objects.update_or_create(user=instance)
        elif instance.role == "Seller":
            Seller.objects.update_or_create(user=instance)
        elif instance.role == "Buyer":
            Buyer.objects.update_or_create(user=instance)
