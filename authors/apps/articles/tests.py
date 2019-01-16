from django.test import TestCase

from articles.models import Article, Tag

class ArticleTestCase(TestCase):

    def setUp(self):
        pass

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
