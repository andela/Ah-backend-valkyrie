from django.test import TestCase

from  rest_framework.reverse import reverse

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article, Tag
from authors.apps.authentication.models import User

class ArticleTestCase(BaseTestMethods):

    def test_get_article(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_user_token(self)
        )
        self.client.post(url, data=self.article, format='json')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.data), 0)

    def test_user_creates_article(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_user_token(self
        ))
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.data['title'], "Test article today")

    def test_create_article_without_login(self):
        url = reverse(self.get_post_article_url)
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, 403)

    def test_create_article_with_incomplete_info(self):
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_user_token(self)
        )
        self.article['body'] = ''
        request = self.client.post(url, data=self.article, format='json')
        self.assertEqual(request.status_code, 400)

    def test_create_article_with_duplicate_title(self):
        pass

    def test_update_article_by_author(self):
        pass

    def test_update_article_by_invalid_author(self):
        pass

    def test_delete_article_by_author(self):
        pass

    def test_delete_article_by_invalid_author(self):
        pass

def get_user_token(self):
    user = User.objects.create_user(**self.user.get('user'))
    return user.token