from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.authentication.backends import JWTAuthentication


class TestUserPasswordReset(BaseTestMethods):
    """
    Test cases for user password reset
    """

    def test_registered_user_recieves_reset_email(self):
        self.register_user()
        url = reverse('reset_password')
        data = {'email': self.user['user']['email']}

        response = self.client.post(url, data=data, format='json')
        email_msg = mail.outbox[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(email_msg.recipients(), ['testuser@andela.com'])

    def test_anonymous_user_cant_recieve_reset_email(self):
        url = reverse('reset_password')
        data = {'email': 'anonymoususer@gmail.com'}

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_password_reset_without_providing_an_email(self):
        url = reverse('reset_password')
        data = {'email': ''}

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_user_cant_reset_password(self):
        token = JWTAuthentication.generate_password_reset_token(
            self.user['user']['email'])
        url = reverse('reset_password_confirm', kwargs={"token": token})
        new_password = {'password': 'testPasswordr3s3t'}

        response = self.client.put(url, data=new_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_registered_user_cant_reset_password_with_invalid_token(self):
        self.register_user()
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI\
        6ImF3ZXNvbWVtZTE1NUBnbWFpbC5jb20iLCJpYXQiOjE1NDc1NTQ1MDk\
        sImV4cCI6MTU0NzU5NzcwOX0'
        url = reverse('reset_password_confirm', kwargs={"token": token})
        new_password = {'password': 'testPasswordr3s3t'}

        response = self.client.put(url, data=new_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registered_user_can_reset_password(self):
        self.register_user()

        token = JWTAuthentication.generate_password_reset_token(
            self.user['user']['email'])
        url = reverse('reset_password_confirm', kwargs={"token": token})
        new_password = {'password': 'testPasswordr3s3t'}

        response = self.client.put(url, data=new_password, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('message'), 'Password reset successful!')
