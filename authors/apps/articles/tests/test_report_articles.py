import json
from rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article, ReportArticle
from authors.apps.authentication.models import User


class TestReportArticle(BaseTestMethods):

    def test_report_article(self):
        """Tests that a user reports an article"""

        user = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            "message": "This post violates the terms and conditions"
        }
        report_url = reverse('articles:report-article',
                             args=[response.data.get('slug')])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        res = self.client.post(report_url, data=data)
        self.assertGreater(len(res.data), 0)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_report_own_article(self):
        """Tests that a user cannot report his own article"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            "message": "This post violates the terms and conditions"
        }
        report_url = reverse('articles:report-article',
                             args=[response.data.get('slug')])
        res = self.client.post(report_url, data=data)
        self.assertEqual(
            res.data.get('detail'),
            'You cannot report your own article'
        )
        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_report_article_without_message(self):
        """Tests that user cannot report article without a message"""

        user = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            "message": ""
        }
        report_url = reverse('articles:report-article',
                             args=[response.data.get('slug')])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        res = self.client.post(report_url, data=data)
        self.assertEqual(
            res.data.get('errors').get('message')[0],
            'This field may not be blank.'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_article_without_message_field(self):
        """Tests that user cannot report article without a message field"""

        user = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        report_url = reverse('articles:report-article',
                             args=[response.data.get('slug')])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        res = self.client.post(report_url)
        self.assertEqual(
            res.data.get('errors').get('message')[0],
            'This field may not be null.'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_article_with_non_existent_slug(self):
        """
        Tests that user cannot report article without a slug
        that does not exist in the database
        """

        user = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            "message": "This post violates the terms and conditions"
        }
        report_url = reverse('articles:report-article',
                             args=['non-existent-slug'])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        res = self.client.post(report_url, data=data)
        self.assertEqual(
            res.data.get('detail'),
            'Article with slug \'non-existent-slug\' was not found'
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_get_reports_for_single_article(self):
        """Tests that admin can retrieve reports for a single article"""

        user1 = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        admin = self.register_superuser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user1.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')

        data = {
            "message": "This post violates the terms and conditions"
        }
        report_url = reverse(
            'articles:report-article',
            args=[response.data.get('slug')]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        self.client.post(report_url, data=data)

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + admin.token)
        res = self.client.get(report_url)
        self.assertEqual(
            res.data[0].get('message'),
            'This post violates the terms and conditions'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_get_reports_for_all_articles(self):
        """Tests that admin can retrieve reports for all articles"""

        user1 = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        admin = self.register_superuser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user1.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')

        data = {
            "message": "This post violates the terms and conditions"
        }
        report_url = reverse(
            'articles:report-article',
            args=[response.data.get('slug')]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        self.client.post(report_url, data=data)

        get_report_url = reverse('articles:reported-articles')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + admin.token)
        res = self.client.get(get_report_url)
        self.assertEqual(
            res.data[0].get('message'),
            'This post violates the terms and conditions'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_get_reports_for_articles(self):
        """Tests that a normal user cannot retrieve reports for articles"""

        user1 = self.register_and_loginUser()
        user2 = self.register_and_login_user2()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user1.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')

        data = {
            "message": "This post violates the terms and conditions"
        }
        report_url = reverse(
            'articles:report-article',
            args=[response.data.get('slug')]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data.get('token'))
        self.client.post(report_url, data=data)

        get_report_url = reverse('articles:reported-articles')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user1.data.get('token'))
        res = self.client.get(get_report_url)
        self.assertEqual(
            res.data.get('detail'),
            'You are not authorized to access this resource'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
