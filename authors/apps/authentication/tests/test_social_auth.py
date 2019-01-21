from .base import BaseTestMethods
from rest_framework import status


class TestSocialAuth(BaseTestMethods):

    def test_login_with_invalid_facebook_token(self):
        # user login with invalid facebook token
        response = self.client.post(
            "/api/v1/auth/facebook/", {"user": {
                "auth_token": self.invalid_facebook_token}}, format='json')
        print(self.valid_facebook_token)
                    
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
                'Invalid or expired token. Please login again.', str(
                    response.data))

    def test_login_with_valid_facebook_token(self):
        # user login with valid facebook token
        
        response = self.client.post(
            "/api/v1/auth/facebook/", {"user": {
                "auth_token": self.valid_facebook_token}}, format='json')
        print(self.valid_facebook_token)
                    
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_google_token(self):
        # user login with invalid google token
        response = self.client.post(
            "/api/v1/auth/google/", {"user": {
                "auth_token": self.invalid_google_token}}, format='json')
        print(self.valid_facebook_token)
                    
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
                'Invalid or expired token. Please login again.', str(
                    response.data))        

    def test_login_with_invalid_twitter_token(self):
        # user login with invalid google token
        response = self.client.post(
            "/api/v1/auth/twitter/", {"user": {
                "auth_token": self.invalid_twitter_token}}, format='json')      
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
                'Invalid or expired token. Please login again', str(
                    response.data)
        )

    def test_login_with_valid_twitter_token(self):
        # user login with invalid google token
        response = self.client.post(
            "/api/v1/auth/twitter/", {"user": {
                "auth_token": self.valid_twitter_token}}, format='json')      
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)
            