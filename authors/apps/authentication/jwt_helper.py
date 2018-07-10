import jwt
from jwt.exceptions import ExpiredSignatureError, ExpiredSignature

from django.conf import settings
from rest_framework import exceptions, status


class JWTHelper:
    def generate_token(self, payload):
        """
        Generates the JWT token
        Args:
            payload(dict): User data
        Returns:
            token: JWT token
        """
        if not payload.get('id') or not payload.get('username') or not payload.get('email'):
            msg = 'Invalid user data'
            raise exceptions.NotAcceptable(
                detail=msg, code=status.HTTP_406_NOT_ACCEPTABLE
            )

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        ).decode()
        return token

    def decode_token(self, token):
        """
        Decodes the token to get user data
        Args:
            token: JWT token
        Returns:
            User data
        """
        try:
            user_data = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
        except ExpiredSignature:
            msg = 'Expired token'
            raise exceptions.AuthenticationFailed(
                msg, status.HTTP_403_FORBIDDEN
            )
        except:
            msg = 'Invalid token'
            raise exceptions.AuthenticationFailed(
                msg, status.HTTP_403_FORBIDDEN
            )
        return user_data
