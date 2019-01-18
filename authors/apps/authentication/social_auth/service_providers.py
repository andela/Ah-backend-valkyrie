from django.http import JsonResponse
import os
import facebook
from google.auth.transport import requests
from google.oauth2 import id_token
import twitter


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


class TwitterAuthTokenVerification:
    """
    class to decode user access_token and user access_token_secret
    tokens will combine the user access_token and access_token_secret separated by space
    """
    @staticmethod
    def extract_twitter_auth_tokens(tokens):
        """
        extract_twitter_auth_tokens methods returns user access token and its secret
        :param tokens: tokens consists of the user access token and access token secret required to validate a user
        """
        auth_tokens = tokens.split(' ')
        if len(auth_tokens) < 2:
            return 'invalid token', 'invalid token'
        user_access_token_key = auth_tokens[0]
        user_access_token_secret = auth_tokens[1]
        return user_access_token_key, user_access_token_secret

    @staticmethod
    def validate_twitter_auth_tokens(tokens):
        """
        validate_twiiter_auth_tokens methods returns a twitter user profile info
        :param tokens: tokens is decoded to get access token and its secret which are validate to get a twitter user profile info.
        """
        access_token_key, access_token_secret = TwitterAuthTokenVerification.extract_twitter_auth_tokens(
            tokens)
        try:
            consumer_api_key = os.environ.get(
                'TWITTER_CONSUMER_API_KEY')
            consumer_api_secret_key = os.environ.get(
                'TWITTER_CONSUMER_API_SECRET_KEY')
            api = twitter.Api(
                consumer_key=consumer_api_key,
                consumer_secret=consumer_api_secret_key,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )

            user_profile_info = api.VerifyCredentials(include_email=True)
            return user_profile_info.__dict__
        except:
            return None