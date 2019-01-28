from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from pprint import pprint

class StatsTestCase(BaseTestMethods):

    def test_get_stats(self):
        article = post_article(self)
        article_slug = article['slug']
        stats_url = reverse(self.get_user_stats)

        # view article
        article_url = reverse(self.single_article_url, args=[article_slug])
        self.client.get(article_url)

        # check change in stats count
        request = self.client.get(stats_url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['count'], 1)
        self.assertEqual(request.data['results'][0]['article']['read_count'], 1)

    def test_retrieve_stats_by_unauthorised_user(self):
        post_article(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='None'
        )
        request = self.client.get(reverse(self.get_user_stats))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

        

def post_article(self):
    url = reverse(self.get_post_article_url)
    self.client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + get_user_token(self)
    )
    request = self.client.post(url, data=self.article, format='json')
    return request.data

def get_user_token(self):
    user = self.register_and_loginUser()
    return user.data['token']