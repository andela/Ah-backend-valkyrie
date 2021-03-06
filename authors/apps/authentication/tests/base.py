from rest_framework.test import APITestCase
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.urls import reverse
from django.core import mail

from authors.apps.authentication.jwt_helper import JWTHelper
from authors.apps.articles.helper import LikeHelper
from .test_data import test_data
from authors.apps.articles.models import Article, FavoriteArticle
from django_currentuser.middleware import get_current_user
from authors.apps.articles.helper import FavoriteHelper
from authors.apps.authentication.models import User

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
            },
            'superuser': {
                'username': 'testsuperuser',
                'email': 'testsuperuser@andela.com',
                'password': 'TestUser124#'
            }
        }
        self.invalid_facebook_token = "EAAEBLo2bPF0BAPEIRTvME7zkOpzyWfkOj8Do7OvaK4xZCXOO3uk4KnTgCqOlnTiurTRCxLNoGRBSt1cUgZBaxgg4s4dUHCdiTtOiZAKTEO5fS2ZCFKsPrRAJzp4ltWTQM7uXLHFoZAcOHPZBZAd4W2LJGTKWZAfr1K8oEP1HZAcuePSEztI7yP9T3"
        self.valid_facebook_token = "EAAEBLo2bPF0BAGYZCZBZAZCjZAcykZCrb67JiJZAerTyigY9Rmsa4a7hP1kR02sZAkUFOTDbFRuEfCJ0UO9OAIOI4dPLKpZAhaYk8eAtfjDjhVe3817j7AkIMyfdtGU55XuMezDHpb9d3rKQV7BHagjO4Q8mkFOxui5LRMKb0dbGGlAZDZD"
        self.invalid_google_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhhYWQ2NmJkZWZjMWI0M2Q4ZGIyN2U2NWUyZTJlZjMwMTg3OWQzZTgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDgxNDY0MDczMTQ5NDIzNzY5NDgiLCJoZCI6ImFuZGVsYS5jb20iLCJlbWFpbCI6ImZhcm9vcS5zc2VydXd1QGFuZGVsYS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IjdHQWNaLWk4QlhDTlhmX0F3UjNIS2ciLCJuYW1lIjoiRmFyb29xIFNzZXJ1d3UiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDYuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy12d1VCaXBYWjBJcy9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBYy9kVnhIaUJBM3I4by9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiRmFyb29xIiwiZmFtaWx5X25hbWUiOiJTc2VydXd1IiwibG9jYWxlIjoiZW4iLCJpYXQiOjE1NDc1NTk2MjIsImV4cCI6MTU0NzU2MzIyMn0.UagvGxjE4KEUsNHW2m2s78WRYteoCTNMN7BSvGwjGVG61pe6MmX31V4iF92-doLZg0SawNbpS4c53oD8kIepgLhWg_EYq6Psgb2vWOKqLKQVMluI1E87fcIaE1wXpGkUeUxUyxfyLpmA46CveEdM40v9bnMy9KMagj3dhedPYEd2Hc9bHbAJdp_CMg2jewYgroBSZ3pSJ6gaXCdN9AN-ZdiveM6s8SUUY5EjE89pLjvhwY0gmbGuabbShcyVY2VQiDooePWvjY7fLW7j5ll2FbnWfwDXBESHrpbkIA8ZhueRJhpV_kvDGKL9A8lQBBszFVc1ce10dJnWOuEpWMkcnw"
        self.valid_twitter_token = "371067164-CGZmMaXIIPfNT0V1OwGHD9PJ66HuNEFMuMz6t6KD EIhr3yUAXNtjw13klhojtihTVnIoz3o8E88J6dR5TCIJX"
        self.invalid_twitter_token = "3710671264-CGZmMaXIIPfNT0V1OwGHD9PJ66HuNEFMuMz6t6KD EIhr3yUAXNtjw13klhojtihTVnIoz3o8E88J6dR5TCIJX"
        self.jwt_helper_class = JWTHelper()
        self.like_helper_class = LikeHelper()
        self.expired_token = test_data.get('expired_token')
        self.non_bearer_token = test_data.get('non_bearer_token')
        self.invalid_token = test_data.get('invalid_token')
        self.non_registered_token = test_data.get('non_registered_token')

        self.article = {
            "title":"Test article today",
            "description":"Testing article creation",
            "body":"This is a lorem ipsum section.",
            "tagList":["sample"],
            "image_url":"https://cdn.ccn.com/wp-content/uploads/2019/01/bitcoin-trader-handcuff-arrest-jail-shutterstock.jpg"
        }

        self.highlight_body = {
            "startIndex":0,
            "endIndex":15,
            "comment":"really basic"
        }

        self.get_post_article_url = "articles:articles_list"
        self.single_article_url = "articles:article_detail"
        self.get_author_articles = "articles:author_articles"
        self.get_tags_url = "articles:tags_list"
        self.get_user_stats = "articles:reading-stats"

        self.model = FavoriteArticle
        self.model2 = Article
        self.favorite = FavoriteHelper()
        self.comment = {
            "comment": {
                "body": "This is a test comment."
            }
        }
        self.comment2 = {
            "comment": {
                "body": "This is another test comment."
            }
        }
        self.jwt_helper_class = JWTHelper()
        self.expired_token = test_data.get('expired_token')
        self.non_bearer_token = test_data.get('non_bearer_token')
        self.invalid_token = test_data.get('invalid_token')
        self.non_registered_token = test_data.get('non_registered_token')

        self.comment3 = {
            "comment": {
                "body": "This is another test comment."
            }
        }
        self.updated_comment = {
            "comment": {
                "body": "Updated this test comment."
            }
        }
        self.highlight_url = "articles:article_highlight"
        
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

    def register_and_login_user2(self):
        self.verify_registered_user2_account()

        url = reverse('user-login')
        data = {
            'user': {
                'email': self.user['user2']['email'],
                'password': self.user['user2']['password']}
        }
        response = self.client.post(url, data=data, format='json')

        return response

    def get_user_acccount_verification_email(self):
        user_data = {
            'user': {
                'email': self.user['user']['email'],
                'password': self.user['user']['password'],
                'username': self.user['user']['username']
            }
        }
        self.create_user(user_data)
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

    def get_user2_acccount_verification_email(self):
        user_data = {
            'user': {
                'email': self.user['user2']['email'],
                'password': self.user['user2']['password'],
                'username': self.user['user2']['username']
            }
        }
        self.create_user(user_data)
        return mail.outbox

    def verify_registered_user2_account(self):
        sent_email = self.get_user2_acccount_verification_email()
        msg = sent_email[1]
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

    def get_user_token(self):
        user = self.register_and_loginUser()
        return user.data['token']

    def get_user2_token(self):
        user = self.register_and_login_user2()
        return user.data['token']

    def create_article(self):
        url = reverse("articles:articles_list")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token()
        )
        request = self.client.post(url, data=self.article, format='json')
        return request

    def favorite_article(self):
        article = self.create_article()
        article_slug = article.data['slug']
        url = reverse("articles:favorite-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(url, format='json')
        return response

    def bookmark_article(self):
        article = self.create_article()
        article_slug = article.data['slug']
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(url, data=self.article, format='json')
        return response

    def post_article(self):
        user = self.register_and_loginUser()
        post_article_url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data['token'])
        article = self.client.post(
            post_article_url, data=self.article, format='json')
        return article.data

    def register_superuser(self):
        return User.objects.create_superuser(**self.user.get('superuser'))
