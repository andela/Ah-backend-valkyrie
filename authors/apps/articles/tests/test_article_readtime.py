from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class ArticleReadTimeTestCase(BaseTestMethods):

    def test_article_has_read_time(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['read_time'], "1 min read")

    def get_user_token(self):
        user = self.register_and_loginUser()
        return user.data['token']
