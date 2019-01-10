# import jwt
#
# from django.conf import settings
#
from rest_framework import authentication, exceptions
#
# from .models import User

"""Configure JWT Here"""
class JWTAuthentication(authentication.BaseAuthentication):
  """Default authentication class to be used in the views"""

  def authenticate(self, request):
    return (None, '')

