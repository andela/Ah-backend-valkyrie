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

    # User registration helper method
    def register_user(self):
        url = reverse('user-registration')
        data = {
            'user': 
            {
                'username': self.user['user']['username'], 
                'email': self.user['user']['email'], 
                'password': self.user['user']['password'],
            }
        }

        response = self.client.post(url, data=data, format='json')

        return response


    def retrieve_user_profile(self):
        self.register_user()
        response = self.client.get('/api/v1/profiles/testuser')

        return response
    

