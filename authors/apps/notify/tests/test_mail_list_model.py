import json

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.authentication.models import User

from rest_framework.reverse import reverse
from rest_framework import status


class NotificationTests(BaseTestMethods):
    def test_create_mail_list(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        auth = f'Bearer {token}'
        url = reverse('mail-list-status')
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(
            response.data['user']['email'], 'testuser@andela.com')

    def test_create_update_notification_status(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        auth = f'Bearer {token}'
        url = reverse('mail-list-status')
        data = {'recieve_email_notifications': 'false'}
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['recieve_email_notifications'], False)

    def test_fetch_all_user_notifications(self):
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        user_2_token = user_2.data['token']
        this_user_2 = User.objects.get(email=user_2.data['email'])

        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username),
            HTTP_AUTHORIZATION=f'Bearer {user_1_token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )
        # fetch notification object
        url = reverse('all-notifications')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')

        self.assertEqual(notifications.status_code, status.HTTP_200_OK)
        self.assertEqual(
            notifications.data['count'], 1)

    def test_cant_fetch_notifications_for_different_user(self):
        # register and login user
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        this_user_2 = User.objects.get(email=user_2.data['email'])
        # follow a registered user
        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username),
            HTTP_AUTHORIZATION=f'Bearer {user_1_token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )
        # fetch user notification objects
        url = reverse('all-notifications')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_1_token}')

        self.assertEqual(
            notifications.data['message'],
            'You currently dont have any notifications')

    def test_fetch_all_user_unread_notifications(self):
        # register and login user
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        user_2_token = user_2.data['token']
        this_user_2 = User.objects.get(email=user_2.data['email'])
        # follow a registered user
        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username),
            HTTP_AUTHORIZATION=f'Bearer {user_1_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )
        # fetch notification object
        url = reverse('unread-notifications')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')

        self.assertEqual(notifications.status_code, status.HTTP_200_OK)
        self.assertEqual(
            notifications.data['count'], 1)

    def test_failed_fetch_all_user_unread_notifications(self):
        # register and login user
        self.register_and_loginUser()

        user_2 = self.register_and_login_user2()
        user_2_token = user_2.data['token']
        # fetch notification object
        url = reverse('unread-notifications')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')

        self.assertEqual(
            notifications.data['message'],
            'You currently dont have any unread notifications')

    def test_fetch_all_user_read_notofications(self):
        # register and login user
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        user_2_token = user_2.data['token']
        this_user_2 = User.objects.get(email=user_2.data['email'])
        # follow a registered user
        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username),
            HTTP_AUTHORIZATION=f'Bearer {user_1_token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )
        # mark notifications as read
        url = reverse('mark-all-as-read')
        self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')

        # fetch notification object
        url = reverse('read-notifications')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')
        self.assertEqual(
            notifications.data['count'], 1)

    def test_failed_fetch_all_user_read_notifications(self):
        # register and login user
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        user_2_token = user_2.data['token']
        this_user_2 = User.objects.get(email=user_2.data['email'])
        # follow a registered user
        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username),
            HTTP_AUTHORIZATION=f'Bearer {user_1_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )
        # fetch notification object
        url = reverse('read-notifications')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')

        self.assertEqual(
            notifications.data['message'], 'You currently dont have any read notifications')

    def test_mark_all_notofications_as_read(self):
        # register and login user
        user_1 = self.register_and_loginUser()
        user_1_token = user_1.data['token']

        user_2 = self.register_and_login_user2()
        user_2_token = user_2.data['token']
        this_user_2 = User.objects.get(email=user_2.data['email'])
        # follow a registered user
        response = self.client.post(
            '/api/v1/users/{}/profile/follow'.format(this_user_2.username),
            HTTP_AUTHORIZATION=f'Bearer {user_1_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)[
                'profile']['following'], True
        )
        # mark notifications as read
        url = reverse('mark-all-as-read')
        notifications = self.client.get(
            url, format='json', HTTP_AUTHORIZATION=f'Bearer {user_2_token}')
        self.assertEqual(
            notifications.data['message'], 'All notifications marked as read')
