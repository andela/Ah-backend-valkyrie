from rest_framework import serializers
from .service_providers import ServiceProviders
from .register import register_user
import facebook
from django.http import JsonResponse


class FacebookSerializer(serializers.Serializer):
    # serialization of facebook data

    auth_token = serializers.CharField()

    def validate_auth_token(self, access_token):
        my_facebook = ServiceProviders()
        user_info = my_facebook.verify(
            provider="facebook", token=access_token
        )
        try:
            user_info['id']
        except:
            raise serializers.ValidationError(
                'Invalid or expired token. Please login again.'
            )
        user_id = user_info['id']
        email = user_info['email']
        name = user_info['email'].split("@")[0]
        my_kwargs = {
            '{0}_{1}'.format('facebook', 'id'): user_id
        }
        return register_user(
            email=email, name=name, **my_kwargs
        )


class GoogleSerializer(serializers.Serializer):
    # serialization of google data.

    auth_token = serializers.CharField()

    def validate_auth_token(self, access_token):
        google = ServiceProviders()
        user_info = google.verify(provider="google", token=access_token)
        try:
            user_info['sub']
        except:
            raise serializers.ValidationError(
                'Invalid or expired token. Please login again.'
            )
        user_id = user_info['sub']
        email = user_info['email']
        name = user_info['email'].split("@")[0]
        my_kwargs = {
            '{0}_{1}'.format('google', 'id'): user_id
        }
        return register_user(
            email=email, name=name, **my_kwargs
        )


class TwitterSerializer(serializers.Serializer):
    # serialization of twitter data

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        twitter = ServiceProviders()
        user_info = twitter.verify(provider="twitter", token=auth_token)
        try:
            user_info['id_str']
        except:
            raise serializers.ValidationError(
                'Invalid or expired token. Please login again'
            )
        user_id = user_info['id_str']
        email = user_info['email']
        name = user_info['email'].split("@")[0]
        my_kwargs = {
            '{0}_{1}'.format('twitter', 'id'): user_id
        }
        return register_user(
            email=email, name=name, **my_kwargs
        )
