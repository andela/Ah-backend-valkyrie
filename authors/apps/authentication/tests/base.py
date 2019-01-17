from rest_framework.test import APITestCase
from django.urls import reverse
from django.core import mail

from authors.apps.authentication.jwt_helper import JWTHelper
from .test_data import test_data


class BaseTestMethods(APITestCase):

    def setUp(self):
        self.user = {
            'user': {
                'username': 'testuser',
                'email': 'testuser@andela.com',
                'password': 'TestUser12#'
            }
        }
        self.jwt_helper_class = JWTHelper()
        self.expired_token = test_data.get('expired_token')
        self.non_bearer_token = test_data.get('non_bearer_token')
        self.invalid_token = test_data.get('invalid_token')
        self.non_registered_token = test_data.get('non_registered_token')
        
    def create_user(self, data):
        """
        Method for creating a new user.
        """
        url = reverse('user-registration')
        response = self.client.post(url, data=data, format="json")
        return response
        
    # User registration and login helper methods
    def register_user(self):
        url = reverse('user-registration')
        data = {
            'user': {
                'username': self.user['user']['username'],
                'email': self.user['user']['email'],
                'password': self.user['user']['password']
            }
        }

        response = self.client.post(url, data=data, format='json')

        return response

    def register_and_loginUser(self):
        self.verify_registered_user_account()

        url = reverse('user-login')
        data = {
            'user': {
                'email': self.user['user']['email'],
                'password': self.user['user']['password']}
        }
        response = self.client.post(url, data=data, format='json')

        return response

    def get_user_acccount_verification_email(self):
        userData = {
            'user': {
                'email': self.user['user']['email'], 
                'password': self.user['user']['password'],
                'username': self.user['user']['username']
            }
        }
        self.create_user(userData)
        return mail.outbox

    def verify_registered_user_account(self):
        sent_email = self.get_user_acccount_verification_email()
        msg = sent_email[0]
        url = (msg.body)[176:]
        splited_url = url.split('/')
        token = splited_url[7]
        user_email = splited_url[8]

        return self.client.get(
            reverse(
                'user-account-verification', 
                args=(token, user_email)
            ), format="json"
        )
