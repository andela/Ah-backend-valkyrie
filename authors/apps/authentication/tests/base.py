from rest_framework.test import APITestCase
from django.urls import reverse

class BaseTestCase(APITestCase):
    
    def setUp(self):
        self.user = {
            "user": {
                "email":  "testuser@andela.com",
                "username": 'testuser',
                'password': 'TestUser12#',
            }
        }

    def createUser(self, data):
        """
        Method for creating a new user.
        """
        url = reverse('user-registration')
        response = self.client.post(url, data=data, format="json")
        return response
