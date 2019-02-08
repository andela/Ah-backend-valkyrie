
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status
from pprint import pprint

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

class TaggingTestCase(BaseTestMethods):
    def test_tagging_for_articles(self):
           url = reverse(self.get_post_article_url)
           self.client.credentials(
               HTTP_AUTHORIZATION='Bearer ' + get_user_token(self
           ))
           self.article['tagList'] = ["Tag1", "Tag2", "Tag3"]
           request = self.client.post(url, data=self.article, format='json')
           self.assertEqual(request.status_code, status.HTTP_201_CREATED)
           self.assertEqual(request.data['tagList'], ["Tag1", "Tag2", "Tag3"])

    def test_updating_tags_for_articles(self):
        url = reverse("articles:articles_list")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_user_token(self)
        )
        request = self.client.post(url, data=self.article, format='json')
        article_slug = request.data['slug']
        self.article['tagList'] = ["Tag1", "Tag2"]
        update_url = reverse(self.single_article_url, args=[article_slug])
        request = self.client.put(update_url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['tagList'], ["Tag1", "Tag2"])

    def test_creating_duplicate_tags(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_user_token(self)
        )
        self.article['tagList'] = ["Tag1"]
        self.client.post(url, data=self.article, format='json')
        request = self.client.post(url, data=self.article, format='json')

        tag_url = reverse(self.get_tags_url)
        tag_request = self.client.get(tag_url)
        self.assertEqual(tag_request.status_code, 200)
        self.assertEqual(len(tag_request.data), 1)


def get_user_token(self):
    user = self.register_and_loginUser()
    return user.data['token']
