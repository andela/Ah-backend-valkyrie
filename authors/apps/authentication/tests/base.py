from rest_framework.test import APITestCase
from django.urls import reverse

from authors.apps.authentication.jwt_helper import JWTHelper
from .test_data import test_data


class BaseTestMethods(APITestCase):

    def setUp(self):
        self.user = {
            'user': {
                'username': 'testuser',
                'email': 'testuser@andela.com',
                'password': 'TestUser12#'
            },
            'user2': {
                'username': 'testuser2',
                'email': 'testuser2@andela.com',
                'password': 'TestUser123#'
            }
        }
        self.jwt_helper_class = JWTHelper()
        self.expired_token = test_data.get('expired_token')
        self.non_bearer_token = test_data.get('non_bearer_token')
        self.invalid_token = test_data.get('invalid_token')
        self.non_registered_token = test_data.get('non_registered_token')

        self.article = {
            "title":"Test article today",
            "description":"Testing article creation",
            "body":"This is a lorem ipsum section.",
            "tagList":[1]
        }
        self.get_post_article_url = "articles:articles_list"
        self.single_article_url = "articles:article_detail"
        self.get_author_articles = "articles:author_articles"
        
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
        self.register_user()

        url = reverse('user-login')
        data = {
            'user': {
                'email': self.user['user']['email'],
                'password': self.user['user']['password']}
        }
        response = self.client.post(url, data=data, format='json')

        return response
