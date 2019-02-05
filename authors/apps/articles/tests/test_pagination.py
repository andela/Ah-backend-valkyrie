from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status
from pprint import pprint

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

class PaginationTestCase(BaseTestMethods):
    def test_get_article(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_user_token(self)
        )
        self.client.post(url, data=self.article, format='json')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        pprint(request.data)
        self.assertEqual(request.data['articlesCount'], 1)


def get_user_token(self):
    user = self.register_and_loginUser()
    return user.data['token']