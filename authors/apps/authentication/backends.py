import jwt
from datetime import datetime
import datetime
from django.conf import settings

from rest_framework import authentication, exceptions, status
from .models import User
from .jwt_helper import JWTHelper

"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):
    """Default authentication class to be used in the views"""
    jwt_helper_class = JWTHelper()

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            #  Authentication was not attempted
            return None

        if len(auth_header) != 2:
            #  Authentication attempted but failed
            msg = 'Invalid token'
            raise exceptions.AuthenticationFailed(
                msg, status.HTTP_403_FORBIDDEN
            )
        prefix = auth_header[0].decode()
        token = auth_header[1].decode()

        if prefix != 'Bearer':
            #  Authentication attempted but failed
            msg = 'Token should be a Bearer token'
            raise exceptions.AuthenticationFailed(
                msg, status.HTTP_403_FORBIDDEN
            )
        return self._get_user_data(request, token)

    def _get_user_data(self, request, token):
        user_data = self.jwt_helper_class.decode_token(token)

        try:
            user = User.objects.get(pk=user_data.get('id'))
        except:
            msg = 'User not found'
            raise exceptions.NotFound(
                msg, status.HTTP_404_NOT_FOUND
            )
        if user.username != user_data.get('username'):
            msg = 'User not found'
            raise exceptions.NotFound(
                msg, status.HTTP_404_NOT_FOUND
            )

        if user.email != user_data.get('email'):
            msg = 'User not found'
            raise exceptions.NotFound(
                msg, status.HTTP_404_NOT_FOUND
            )

        if not user.is_active:
            msg = 'This user has been deactivated'
            raise exceptions.NotAcceptable(
                detail=msg, code=status.HTTP_406_NOT_ACCEPTABLE
            )
        return (user, token)

        # User password reset token generator
    @classmethod
    def generate_password_reset_token(cls, email):
        token = jwt.encode({
            'email': email,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=700)
        },
            settings.SECRET_KEY,
            algorithm='HS256'
        ).decode()

        return token
