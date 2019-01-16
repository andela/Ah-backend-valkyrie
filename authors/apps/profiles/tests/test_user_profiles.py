import json

from rest_framework import status

from authors.apps.profiles.tests.base import BaseTestMethods


class TestUserProfile(BaseTestMethods):
    """
    Test cases for user retrieving an existing profile
    """

    def test_retrieve_an_existing_profile(self):
        response = self.retrieve_user_profile()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)['profile']['username'],
            "testuser"
        )
        self.assertEqual(
            json.loads(response.content)['profile']['bio'],
            ""
        )

    def test_a_non_existent_profile(self):
        response = self.client.get('/api/v1/profiles/testusers1')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)['errors']['detail'],
            "The profile you requested does not exist."
        )