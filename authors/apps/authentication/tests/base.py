from rest_framework.test import APITestCase
from django.urls import reverse


class BaseTestMethods(APITestCase):
   
    def setUp(self):
        self.user = {
            'user':{
                'username':'testuser', 
                'email':'testuser@andela.com' , 
                'password':'TestUser12#'
            }
        }

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


