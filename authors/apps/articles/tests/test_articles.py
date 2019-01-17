from django.test import TestCase

from  rest_framework.reverse import reverse

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article, Tag
from authors.apps.authentication.models import User

class ArticleTestCase(BaseTestMethods):

    def test_get_article(self):
        user = User.objects.create_user(**self.user.get('user'))
        url = reverse('articles:articles_list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + user.token)
        self.client.post(url, data=self.article, format='json')
        response = self.client.get(url)
        self.assertGreater(len(response.data), 0)

    def test_user_creates_article(self):
        pass

    def test_user_with_incomplete_info(self):
        pass

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
