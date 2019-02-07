from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from pprint import pprint

class HighlightTestCase(BaseTestMethods):

    def test_post_highlight_article(self):
        article = post_article(self)
        article_slug = article['slug']
        highlight_url = reverse(self.highlight_url, args=[article_slug])
        request = self.client.post(
            highlight_url,
            data=self.highlight_body,
            format='json'
        )
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.data['comment'], "really basic")
        self.assertEqual(request.data['selected_text'], "This is a lorem")

    def test_post_highlight_article_with_comment_optional(self):
        article = post_article(self)
        article_slug = article['slug']
        del self.highlight_body['comment']
        highlight_url = reverse(self.highlight_url, args=[article_slug])
        request = self.client.post(
            highlight_url,
            data=self.highlight_body,
            format='json'
        )
        pprint(request.data)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.data['comment'], "")

    def test_post_highlight_article_with_missing_indices(self):
        article = post_article(self)
        article_slug = article['slug']
        del self.highlight_body['startIndex']
        del self.highlight_body['endIndex']
        highlight_url = reverse(self.highlight_url, args=[article_slug])
        request = self.client.post(
            highlight_url,
            data=self.highlight_body,
            format='json'
        )
        self.assertEqual(request.status_code, 400)

    def test_post_highlight_article_with_unauthorised_user(self):
        article = post_article(self)
        article_slug = article['slug']
        self.client.credentials(
            HTTP_AUTHORIZATION='None'
        )
        highlight_url = reverse(self.highlight_url, args=[article_slug])
        request = self.client.post(
            highlight_url,
            data=self.highlight_body,
            format='json'
        )
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