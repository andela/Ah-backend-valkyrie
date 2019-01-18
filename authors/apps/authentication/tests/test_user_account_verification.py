from .base import BaseTestMethods
from django.urls import reverse
from rest_framework import status

class TestUserAccountVerification(BaseTestMethods):

    def test_successful_registration_email(self):
        # Test if email is sent to user email address
        sent_email = self.get_user_acccount_verification_email()
        self.assertEquals(len(sent_email), 1)
        msg = sent_email[0]
        self.assertEquals(msg.recipients(), ['testuser@andela.com'])
        self.assertEqual(msg.subject, 'Author\'s Haven Account Verification.')
        self.assertIn('Hello Testuser!', msg.body)

    def test_account_verification_success(self):
        #Test successful user account verification
        sent_email = self.get_user_acccount_verification_email()
        self.assertEquals(len(sent_email), 1)
        msg = sent_email[0]
        url = (msg.body)[175:]
        splited_url = url.split('/')
        token = splited_url[7]
        user_email = splited_url[8]
        response_data = {
            "message": "Your account has been verified successfully."
        }
        verifcation_response = self.client.get(
            reverse(
                'user-account-verification', 
                args=(token, user_email)
            ), format="json"
        )
        self.assertEquals(
            verifcation_response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(verifcation_response.data, response_data)


    def test_account_verification_with_invalid_token(self):
        sent_email = self.get_user_acccount_verification_email()
        self.assertEquals(len(sent_email), 1)
        msg = sent_email[0]
        url = (msg.body)[175:]
        splited_url = url.split('/')
        token = '530-1d6cf43f07fb19e03b4a'
        user_email = splited_url[8]
        response_data = {
            "message": "Invalid Token used."
        }
        verifcation_response = self.client.get(
            reverse(
                'user-account-verification', 
                args=(token, user_email)
            ), format="json"
        )
        self.assertEquals(
            verifcation_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEquals(verifcation_response.data, response_data)

    def test_account_verification_with_invalid_user_decoded_email(self):
        sent_email = self.get_user_acccount_verification_email()
        self.assertEquals(len(sent_email), 1)
        msg = sent_email[0]
        url = (msg.body)[175:]
        splited_url = url.split('/')
        token = splited_url[7]
        user_email = 'bWFuemVkZUBnbWFpbC5jb20'
        response_data = {
            "message": "Cannot find this user"
        }
        verifcation_response = self.client.get(
            reverse(
                'user-account-verification', 
                args=(token, user_email)
            ), format="json"
        )
        self.assertEquals(
            verifcation_response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        self.assertEquals(verifcation_response.data, response_data)
