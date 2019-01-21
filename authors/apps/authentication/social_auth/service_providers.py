from django.http import JsonResponse
import os
import facebook
from google.auth.transport import requests
from google.oauth2 import id_token
import twitter
from decouple import config


class ServiceProviders:
    
    def verify(self, provider, token):
        # verify all service provider tokens.
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
        elif provider == "twitter":
            access_token_key, access_token_secret = self.split_twitter_auth_tokens(
                tokens=token
            )
            try:
                consumer_api_key = config(
                    'TWITTER_CONSUMER_API_KEY')
                consumer_api_secret_key = config(
                    'TWITTER_CONSUMER_API_SECRET_KEY')
                api = twitter.Api(
                    consumer_key=consumer_api_key,
                    consumer_secret=consumer_api_secret_key,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret
                )

                user_profile_info = api.VerifyCredentials(include_email=True)
                return user_profile_info.__dict__
            except Exception as excp:
                print(str(excp))
                return None            
      
    def split_twitter_auth_tokens(self, tokens):
        # split the twitter token into the secret token and key token
        auth_tokens = tokens.split(' ')
        if len(auth_tokens) < 2:
            return 'invalid token', 'invalid token'
        access_token_key = auth_tokens[0]
        access_token_secret = auth_tokens[1]
        return access_token_key, access_token_secret
        