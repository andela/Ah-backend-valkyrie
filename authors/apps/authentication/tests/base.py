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
            }
        }
        self.invalid_facebook_token = "EAAEBLo2bPF0BAPEIRTvME7zkOpzyWfkOj8Do7OvaK4xZCXOO3uk4KnTgCqOlnTiurTRCxLNoGRBSt1cUgZBaxgg4s4dUHCdiTtOiZAKTEO5fS2ZCFKsPrRAJzp4ltWTQM7uXLHFoZAcOHPZBZAd4W2LJGTKWZAfr1K8oEP1HZAcuePSEztI7yP9T3"
        self.valid_facebook_token = "EAAEBLo2bPF0BAGYZCZBZAZCjZAcykZCrb67JiJZAerTyigY9Rmsa4a7hP1kR02sZAkUFOTDbFRuEfCJ0UO9OAIOI4dPLKpZAhaYk8eAtfjDjhVe3817j7AkIMyfdtGU55XuMezDHpb9d3rKQV7BHagjO4Q8mkFOxui5LRMKb0dbGGlAZDZD"
        self.invalid_google_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhhYWQ2NmJkZWZjMWI0M2Q4ZGIyN2U2NWUyZTJlZjMwMTg3OWQzZTgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDgxNDY0MDczMTQ5NDIzNzY5NDgiLCJoZCI6ImFuZGVsYS5jb20iLCJlbWFpbCI6ImZhcm9vcS5zc2VydXd1QGFuZGVsYS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IjdHQWNaLWk4QlhDTlhmX0F3UjNIS2ciLCJuYW1lIjoiRmFyb29xIFNzZXJ1d3UiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDYuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy12d1VCaXBYWjBJcy9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBYy9kVnhIaUJBM3I4by9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiRmFyb29xIiwiZmFtaWx5X25hbWUiOiJTc2VydXd1IiwibG9jYWxlIjoiZW4iLCJpYXQiOjE1NDc1NTk2MjIsImV4cCI6MTU0NzU2MzIyMn0.UagvGxjE4KEUsNHW2m2s78WRYteoCTNMN7BSvGwjGVG61pe6MmX31V4iF92-doLZg0SawNbpS4c53oD8kIepgLhWg_EYq6Psgb2vWOKqLKQVMluI1E87fcIaE1wXpGkUeUxUyxfyLpmA46CveEdM40v9bnMy9KMagj3dhedPYEd2Hc9bHbAJdp_CMg2jewYgroBSZ3pSJ6gaXCdN9AN-ZdiveM6s8SUUY5EjE89pLjvhwY0gmbGuabbShcyVY2VQiDooePWvjY7fLW7j5ll2FbnWfwDXBESHrpbkIA8ZhueRJhpV_kvDGKL9A8lQBBszFVc1ce10dJnWOuEpWMkcnw"
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
        self.register_user()

        url = reverse('user-login')
        data = {
            'user': {
                'email': self.user['user']['email'],
                'password': self.user['user']['password']}
        }
        response = self.client.post(url, data=data, format='json')

        return response
