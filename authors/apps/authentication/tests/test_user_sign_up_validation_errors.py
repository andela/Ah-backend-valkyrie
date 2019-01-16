from authors.apps.authentication.tests.base import BaseTestMethods
from rest_framework import status

class UserRegistrationAPIViewTestCase(BaseTestMethods):

    def test_user_sign_up_without_input(self):
        """
        Test for user registration validation errors.
        """
        data = {"user": { }}
        dummy_user_data_response = {
            "errors": {
                "email": ["This field is required."],
                "username": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, dummy_user_data_response)

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
        email_exists_response = {
            "errors": {"email": ["user with this email already exists."]}
        }
        self.create_user(self.user)
        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, email_exists_response)

    def test_user_sign_up_username_exists(self):
        """
        Test an existing user with this username.
        """
        username_exists_data = {
            "user": {
                "email":  "testnewuser@andela.com",
                "username": 'testuser',
                'password': 'TESTuser123#',
            }
        }
        username_exists_response = {
            "errors": {
                "username": ["user with this username already exists."]
            }
        }
        self.create_user(self.user)
        response = self.create_user(username_exists_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, username_exists_response)
    
    def test_user_sign_up_password_length(self):
        """
        Test an if password length is less than 8 charaters.
        """
        password_length_data = {
            "user": {
                "email":  "testuser_new_1@andela.com",
                "username": 'testuser_new_1',
                'password': 'test',
            }
        }
        password_length_response = {
            "errors": { 
                "password":["Ensure this field has at least 8 characters."]
            }
        }
        response = self.create_user(password_length_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, password_length_response)

    def test_user_sign_up_password_strength(self):
        """
        Test an if password is strong and contains numbers, 
        letters and sepcial characters.
        """
        password_strength_data = {
            "user": {
                "email":  "testuser_new_1@andela.com",
                "username": 'testuser_new_1',
                'password': 'testings',
            }
        }
        password_strength_response = {
            "errors": {
                "password": [
                    'Password must have numbers, ' +
                    'letters and special characters.'
                ]
            }
        }
        response = self.create_user(password_strength_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, password_strength_response)
