from .base import BaseTestCase
from rest_framework import status

from . import *

class UserRegistrationAPIViewTestCase(BaseTestCase):

    def test_user_sign_up_without_input(self):
        """
        Test for user registration validation errors.
        """
        data = {"user": { }}
        dummyUserDataResponse = {
            "errors": {
                "email": ["This field is required."],
                "username": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        response = self.createUser(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, dummyUserDataResponse)

    def test_user_sign_up_email_exists(self):
        """
        Test an existing user email address.
        """
        data = {
            "user": {
                "email":  "testuser@andela.com",
                "username": 'testuser_new',
                'password': 'TESTuser123#',
            }
        }
        emailExistsResponse = {
            "errors": { "email": ["user with this email already exists."] }
        }
        self.createUser(self.user)
        response = self.createUser(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, emailExistsResponse)

    def test_user_sign_up_username_exists(self):
        """
        Test an existing user with this username.
        """
        usernameExistsData = {
            "user": {
                "email":  "testnewuser@andela.com",
                "username": 'testuser',
                'password': 'TESTuser123#',
            }
        }
        usernameExistsResponse = {
            "errors": {"username": ["user with this username already exists."]}
        }
        self.createUser(self.user)
        response = self.createUser(usernameExistsData)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, usernameExistsResponse)
    
    def test_user_sign_up_password_length(self):
        """
        Test an if password length is less than 8 charaters.
        """
        passwordLenghtData = {
            "user": {
                "email":  "testuser_new_1@andela.com",
                "username": 'testuser_new_1',
                'password': 'test',
            }
        }
        passwordLengthResponse = {
            "errors": { "password": ["Ensure this field has at least 8 characters."]}
        }
        response = self.createUser(passwordLenghtData)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, passwordLengthResponse)

    def test_user_sign_up_password_strength(self):
        """
        Test an if password is strong and contains numbers and letters.
        """
        passwordStrengthData = {
            "user": {
                "email":  "testuser_new_1@andela.com",
                "username": 'testuser_new_1',
                'password': 'testings',
            }
        }
        passwordStrengthResponse = {
            "errors": {
                "password": ["Password must contain a number, letters and a special character."]
            }
        }
        response = self.createUser(passwordStrengthData)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, passwordStrengthResponse)

