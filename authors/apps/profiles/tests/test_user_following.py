import json

from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.authentication.models import User
from ..models import Profile


class TestUserFollowing(BaseTestMethods):

    def test_registered_user_can_follow_another_registered_user(self):
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        this_user_2 = User.objects.get(email=user_2.data['email'])

        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username), HTTP_AUTHORIZATION=f'Bearer {user_1_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )

    def test_a_registered_user_can_unfollow_a_user_they_follow(self):
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        this_user_2 = User.objects.get(email=user_2.data['email'])
        this_user_2.following = True

        response = self.client.delete(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username), HTTP_AUTHORIZATION=f'Bearer {user_1_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], False
        )

    def test_a_user_cannot_follow_themselves(self):
        user = self.register_and_loginUser()
        user_token = user.data['token']
        this_user = User.objects.get(email=user.data['email'])

        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user.username), HTTP_AUTHORIZATION=f'Bearer {user_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['detail'], "You cannot follow yourself."
        )

    def test_follow_a_profile_of_a_non_existing_user(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format('non_existing_username'),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)['errors']['detail'],
            "The profile you requested does not exist."
        )

    def test_get_all_followers_of_a_user(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        response = self.client.get(
            '/api/v1/users/me/profile/followers', HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['followers'], [])

    def test_get_all_followings_of_a_user(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        response = self.client.get(
            '/api/v1/users/me/profile/followings', HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['followings'], [])
