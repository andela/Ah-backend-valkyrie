import json

from rest_framework import status

from authors.apps.profiles.tests.base import BaseTestMethods
from authors.apps.authentication.models import User


class TestUserProfile(BaseTestMethods):
    """
    Test cases for user retrieving an existing profile
    """

    def test_retrieve_profile_of_an_existing_user(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        this_user = User.objects.get(email=user.data['email'])
        response = self.client.get(
            '/api/v1/users/{}/profile/'.format(this_user.id),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)['profile']['username'],
            "testuser"
        )

    def test_retrieve_profile_of_a_non_existing_user(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        response = self.client.get(
            '/api/v1/users/{}/profile/'.format(2),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)['errors']['detail'],
            "The profile you requested does not exist."
        )

    def test_retrieve_profile_of_an_existing_user_with_invalid_token(self):
        user = self.register_and_loginUser()
        token = self.invalid_token
        this_user = User.objects.get(email=user.data['email'])
        response = self.client.get(
            '/api/v1/users/{}/profile/'.format(this_user.id),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Invalid token', response.data.get('detail'))

    def test_user_can_update_their_profile(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        this_user = User.objects.get(email=user.data['email'])
        data = {
            "user": {
                "bio": "I love music",
                "image": "http://images.com/profile.jpg"
            }
        }
        response = self.client.put(
            '/api/v1/users/{}/'.format(this_user.id), data=data, format='json',
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[
                         'user']['bio'], "I love music")

    def test_user_cannot_update_another_users_profile(self):
        owner = self.register_and_loginUser()
        owner_token = owner.data['token']

        non_owner = self.register_and_login_user2()
        this_non_owner = User.objects.get(email=non_owner.data['email'])

        profile_data = {
            'user': {
                'username': 'frank',
                'email': 'frank@andela.com',
                'password': 'TestUser12#'
            }
        }
        response = self.client.put(
            '/api/v1/users/{}/'.format(this_non_owner.id), data=profile_data, format='json',
            HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content)['user']['detail'],
            "You are not allowed perform this action"
        )
