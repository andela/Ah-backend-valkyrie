from django.db import models

from ..authentication.models import User


class Profile(models.Model):

    """
    There is a one to one relationship between the User and the Profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    following = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
