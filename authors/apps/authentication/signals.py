from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.apps.profiles.models import Profile
from .models import User


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    """
    Check for 'created the first time the 'User' instance is created.
    If an update action takes place, we will know that the user already has a profile
    """
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
