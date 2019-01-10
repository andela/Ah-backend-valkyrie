from rest_framework import status
from rest_framework.reverse import reverse

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base import BaseTestMethods


class TestUserRegistration(BaseTestMethods):
    """
    Test cases for user registration and login
    """
    
    def test_ordinary_user(self):
        user = User.objects.create_user(**self.user['user'])
       
        self.assertEqual(user.__str__(), self.user['user']['email'])
        self.assertEqual(user.get_full_name, self.user['user']['username'])
        self.assertEqual(user.get_short_name(), self.user['user']['username'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_super_user(self):
        super_user = User.objects.create_superuser(**self.user['user'])

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
    
    def test_successful_user_registration(self):
        response = self.register_user()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {'email': self.user['user']['email'],
                            'username': self.user['user']['username']
                            }
            )
        self.assertIsInstance(response.data, dict)

    def test_successful_user_login(self):
        response = self.register_and_loginUser()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {
                'email': self.user['user']['email'],
                'username': self.user['user']['username']
            }
        )
        

    def test_login_with_un_matching_email(self):

        self.register_user()

        url = reverse('user-login')
        data = {
            'user': 
    {'email': 'invalid@test.com', 'password': self.user['user']['password']}}
        response = self.client.post(url, data=data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertIn(
            'A user with this email and password was not found.',
            response.data['errors']['error'][0]
            )

    def test_login_without_an_email(self):

        self.register_user()
        
        url = reverse('user-login')
        data = {'user': {'password': self.user['user']['password']}}
        response = self.client.post(url, data=data, format='json')
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field is required.', response.data['errors']['email'][0])

    def test_login_without_a_password(self):
        self.register_user()
        
        url = reverse('user-login')
        data = {'user': {'email': self.user['user']['email']}}
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field is required.', response.data['errors']['password'][0])


    


    


    


        


