from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status
import json
from django_social_share.templatetags import social_share

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile


class TestArticleShare(BaseTestMethods):

    def shareArticle(self):
        user = self.register_and_loginUser()
        token = user.data['token']
        data = self.article
        providers = ['facebook', 'twitter', 'email', 'wikipedia']
        response = self.client.post(
            '/api/v1/articles/',
            data=data, format='json',
            HTTP_AUTHORIZATION=f'Bearer {token}')

        slug = response.data['slug']

        return {'token': token, 'slug': slug, 'providers': providers}

    def test_an_article_can_be_shared_on_facebook(self):
        slug = self.shareArticle()['slug']
        token = self.shareArticle()['token']
        provider = self.shareArticle()['providers'][0]

        link = "https://www.facebook.com/sharer/sharer.php?u=http%3A//testserver/articles/test-article-today/"

        response = self.client.get(
            '/api/v1/articles/{0}/share/{1}/'.format(slug, provider),
            HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)
                         ['link'], link)

    def test_an_article_can_be_shared_on_twitter(self):
        slug = self.shareArticle()['slug']
        token = self.shareArticle()['token']
        provider = self.shareArticle()['providers'][1]

        link = "https://twitter.com/intent/tweet?text=http%3A//testserver/articles/test-article-today/"

        response = self.client.get(
            '/api/v1/articles/{0}/share/{1}/'.format(slug, provider),
            HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)
                         ['link'], link)

    def test_an_article_can_be_shared_via_email(self):
        slug = self.shareArticle()['slug']
        token = self.shareArticle()['token']
        provider = self.shareArticle()['providers'][2]

        link = "mailto:?subject=%20shared%20Test%20article%20today%20with%20you.&body=Read%20Test%20article%20today%20shared%20by%20%20%20http%3A//testserver/articles/test-article-today/"

        response = self.client.get(
            '/api/v1/articles/{0}/share/{1}/'.format(slug, provider),
            HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)
                         ['link'], link)

    def test_sharing_via_invalid_provider(self):

        slug = self.shareArticle()['slug']
        token = self.shareArticle()['token']
        provider = self.shareArticle()['providers'][3]
        response = self.client.get(
            '/api/v1/articles/{0}/share/{1}/'.format(slug, provider),
            HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)
                         ['error'], 'Invalid provider link')

    def test_sharing_non_existent_article(self):
        token = self.shareArticle()['token']
        provider = self.shareArticle()['providers'][0]
        response = self.client.get(
            '/api/v1/articles/{0}/share/{1}/'.format('No_Slug', provider),
            HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content)
                         ['message'], 'This article doesnot exist.')
