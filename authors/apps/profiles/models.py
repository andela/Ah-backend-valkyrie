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

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    following = models.ManyToManyField(
        'self', related_name='followers', symmetrical=False)

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.following.add(profile)

    def unfollow(self, profile):
        self.following.remove(profile)

    def is_following(self, profile):
        return self.following.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        return self.following.filter(pk=profile.pk).exists()
