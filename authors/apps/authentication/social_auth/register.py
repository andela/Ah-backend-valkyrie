from django.contrib.auth import authenticate
from rest_framework.response import Response
from authors.apps.authentication.models import User


def register_user(email, name, **kwargs):
    # register social media user.
    user = User.objects.filter(**kwargs)
    if not user.exists():
        user = {
            'username': name, 'email': email, 'password': 'aaaaaaaa'}
        User.objects.create_user(**user)
        User.objects.filter(email=email).update(**kwargs)
        User.objects.filter(email=email).update(is_active=True)
        new_user = authenticate(email=email, password="aaaaaaaa")
        return new_user.get_token
    User.objects.filter(**kwargs)
    registered_user = authenticate(email=email, password="aaaaaaaa")
    return registered_user.get_token
