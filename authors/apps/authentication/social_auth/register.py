from django.contrib.auth import authenticate
from rest_framework.response import Response
from authors.apps.authentication.models import User


def register_user(email, name, **kwargs):
    # register social media user.
    try:
        User.objects.get(email=email)
        login_user = authenticate(
            email=email,
            password="aaaaaaa"
        )
        return login_user.token
    except:
        user = {
            'username': name,
            'email': email,
            'password': "aaaaaaa"
        }
        User.objects.create_user(**user)
        User.objects.filter(email=email).update(**kwargs)
        User.objects.filter(email=email).update(is_active=True)
        new_user = authenticate(email=email, password="aaaaaaa")
        return new_user.token
