from django.http import JsonResponse
import os
import facebook
from google.auth.transport import requests
from google.oauth2 import id_token


class ServiceProviders:
    """Google class to fetch the user info and return it"""

    def verify(self, provider, token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        :param str auth_token: The access token of the Google user
        """
        if provider == "google":
            try:
                id_info = id_token.verify_oauth2_token(
                    token, requests.Request())
                if id_info['iss'] not in [
                    'accounts.google.com', 'https://accounts.google.com'
                     ]:
                    raise ValueError('Wrong issuer.')

                user_id = id_info['sub']
                return id_info
            except ValueError:
                return "The token is either invalid or has expired"
        elif provider == "facebook":
            try:
                graph = facebook.GraphAPI(access_token=token)
                user_info = graph.get_object(
                    id='me',
                    fields='name, id, '
                    'email'
                    )
                return user_info
            except facebook.GraphAPIError:
                return JsonResponse(
                    {
                        'error': 'Invalid or expired token. Please login again'
                        }, safe=False
                    )
