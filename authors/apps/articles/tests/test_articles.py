from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class ArticleTestCase(BaseTestMethods):

    def test_get_article(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token()
        )
        self.client.post(url, data=self.article, format='json')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.data), 0)

    def test_get_author_article(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        url = reverse(self.get_post_article_url)
        request = self.client.post(url, data=self.article, format='json')
        author_id = request.data['author']['username']
        author_articles = reverse(self.get_author_articles, args=[author_id])
        request = self.client.get(author_articles)
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.data), 0)
        self.assertEqual(request.data['results']
                         [0]['author']['username'], author_id)

    def test_user_creates_article(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['title'], "Test article today")

    def test_create_article_without_login(self):
        url = reverse(self.get_post_article_url)
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, 403)

    def test_create_article_with_incomplete_info(self):
        # create with incomplete information
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token()
        )
        self.article['body'] = ''
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_with_duplicate_title(self):
        # create article
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token()
        )
        self.client.post(url, data=self.article, format='json')
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['slug'], "test-article-today-3")

    def test_update_article_by_author(self):
        # create article
        response = self.create_article()
        article_slug = response.data['slug']
        self.article['title'] = "Test article yesterday"
        # update article
        update_url = reverse(self.single_article_url, args=[article_slug])
        request = self.client.put(update_url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], "Test article yesterday")

    def test_update_article_by_invalid_author(self):

        # create article with first user
        response = self.create_article()
        article_slug = response.data['slug']

        # create second user and update first user's article
        user2_token = self.get_user2_token()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2_token
        )
        self.article['title'] = "Test article yesterday"
        update_url = reverse(self.single_article_url, args=[article_slug])
        request = self.client.put(update_url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            request.data['detail'],
            "You do not have permission to perform this action."
        )

    def test_delete_article_by_author(self):
        # create article
        response = self.create_article()
        article_slug = response.data['slug']
        # delete article
        delete_url = reverse(self.single_article_url, args=[article_slug])
        request = self.client.delete(
            delete_url,
            data=self.article,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_article_by_invalid_author(self):
        # create article with first user
        response = self.create_article()
        article_slug = response.data['slug']
        # create second user and delete first user's article
        user2 = self.get_user2_token()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2
        )
        delete_url = reverse(self.single_article_url, args=[article_slug])
        request = self.client.put(delete_url, data=self.article, format='json')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            request.data['detail'],
            "You do not have permission to perform this action."
        )
