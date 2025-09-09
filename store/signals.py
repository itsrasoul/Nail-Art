from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile, Cart

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Cart.objects.get_or_create(user=instance)
