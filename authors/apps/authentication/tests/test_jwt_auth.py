#pylint: disable=E1101
from datetime import datetime, timedelta

from rest_framework import status, exceptions
from rest_framework.reverse import reverse

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base import BaseTestMethods


class TestJWTAuthentication(BaseTestMethods):
    """Test cases for JWT Authentication"""

    def test_generate_token(self):
        """Tests that a JWT token is generated successfully"""

        user = User.objects.create_user(**self.user.get('user'))
        payload = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        token = self.jwt_helper_class.generate_token(payload).split('.')
        self.assertEqual(3, len(token))

    def test_generate_token_failure(self):
        """Tests that a JWT was not generated"""

        user = User.objects.create_user(**self.user.get('user'))
        payload = {
            'email': user.email,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        with self.assertRaises(exceptions.NotAcceptable):
            self.jwt_helper_class.generate_token(payload)

    def test_expired_token(self):
        """Tests that the token is expired or invalid"""

        with self.assertRaises(exceptions.AuthenticationFailed):
            self.jwt_helper_class.decode_token(self.expired_token)

    def test_decode_token_success(self):
        """Tests that the token is decoded successfully"""

        user = User.objects.create_user(**self.user.get('user'))
        payload = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        token = self.jwt_helper_class.generate_token(payload)
        user_data = self.jwt_helper_class.decode_token(token)
        self.assertEqual(user_data.get('id'), user.id)

    def test_that_login_returns_token(self):
        """Tests that a user receives a token on successful login"""
        self.register_and_loginUser()
        response = self.register_and_loginUser()
        self.register_user()
        self.register_and_loginUser()
        url = reverse('user-login')
        data = {
            'user': {
                'email': self.user.get('user').get('email'),
                'password': self.user.get('user').get('password')
            }
        }
        response = self.client.post(url, data=data, format='json')
        self.assertIn('token', response.data)
        self.assertEqual(3, len(response.data.get('token').split('.')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_registration_returns_token(self):
        """Tests that a user receives a token on successful registration"""

        response = self.register_user()
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_bearer_token(self):
        """Tests that the token is not a bearer token"""
        user = User.objects.create_user(**self.user.get('user'))
        url = reverse(
            'update-retrieve-user',
            kwargs={'pk': user.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=self.non_bearer_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Token should be a Bearer token',
                         response.data.get('detail'))

    def test_invalid_token(self):
        """Tests that the token is not a valid token"""

        user = User.objects.create_user(**self.user.get('user'))
        url = reverse(
            'update-retrieve-user',
            kwargs={'pk': user.id}
        )
        self.client.credentials(HTTP_AUTHORIZATION=self.invalid_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Invalid token',
                         response.data.get('detail'))

    def test_token_does_not_belong_to_registered_user(self):
        """
        Tests that the person in possession of this token is
        not a registered user
        """

        self.register_user()
        url = reverse(
            'update-retrieve-user',
            kwargs={'pk': 10}
        )
        self.client.credentials(HTTP_AUTHORIZATION=self.non_registered_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            'User not found',
            response.data.get('detail')
        )

    def test_user_account_is_deactivated(self):
        """
        Tests that the account associated with this token has
        been deactivated
        """

        user = User.objects.create_user(**self.user.get('user'))
        url = reverse(
            'update-retrieve-user',
            kwargs={'pk': user.id}
        )
        data = {
            'user': {
                'is_active': False,
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + user.token)
        self.client.put(url, data=data, format='json')
        login_url = reverse('user-login')
        data = {
            'user': {
                'email': self.user.get('user').get('email'),
                'password': self.user.get('user').get('password')
            }
        }
        response = self.client.post(login_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual('This user has been deactivated',
                         response.data.get('detail'))
