import json
from rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article, LikeArticle
from authors.apps.authentication.models import User


class TestLikeArticle(BaseTestMethods):

    def test_like_article(self):
        """Tests that an article has been liked successfuly"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:like-article', kwargs=data)
        res = self.client.post(like_url)
        self.assertTrue(res.data.get('like'), True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unlike_article(self):
        """Tests that a like is removed from an article"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:like-article', kwargs=data)
        self.client.post(like_url)
        #  Like same article a second time
        res = self.client.post(like_url)
        self.assertTrue(res.data.get('like'), True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unlike_article(self):
        """Tests that a like is removed from an article"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:like-article', kwargs=data)
        self.client.post(like_url)
        #  Like same article a second time
        res = self.client.post(like_url)
        self.assertTrue(res.data.get('like'), True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_dislike_article(self):
        """Tests that an article has been disliked successfuly"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:dislike-article', kwargs=data)
        res = self.client.post(like_url)
        self.assertFalse(res.data.get('like'), False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_un_dislike_article(self):
        """Tests that a dislike is removed from an article"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:dislike-article', kwargs=data)
        self.client.post(like_url)
        #  Dislike same article a second time
        res = self.client.post(like_url, data=data, format='json')
        self.assertFalse(res.data.get('like'), False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_likes(self):
        """
        Tests that likes for a particular article are
        fetched from the database
        """
        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:like-article', kwargs=data)
        self.client.post(like_url)
        article = self.like_helper_class.get_article_by_slug(
            model=Article,
            slug=response.data.get('slug')
        )
        likes = self.like_helper_class.get_likes_or_dislike(
            model=LikeArticle,
            like=True,
            article_id=article.id
        )
        self.assertEqual(likes.get('count'), 1)

    def test_get_dislikes(self):
        """
        Tests that likes for a particular article are
        fetched from the database
        """
        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:dislike-article', kwargs=data)
        self.client.post(like_url)
        article = self.like_helper_class.get_article_by_slug(
            model=Article,
            slug=response.data.get('slug')
        )
        likes = self.like_helper_class.get_likes_or_dislike(
            model=LikeArticle,
            like=False,
            article_id=article.id
        )
        print(likes)
        self.assertEqual(likes.get('count'), 1)

    def test_like_article_with_invalid_slug(self):
        """
        Tests that like article fails for a slug that
        does not exists
        """
        user = self.register_and_loginUser()
        data = {
            'slug': 'this-does-not-exist'
        }
        like_url = reverse('articles:like-article', kwargs=data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(like_url)
        self.assertTrue(
            response.data.get('detail'),
            'Article with slug \'this-does-not-exist\' was not found'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_dislike_article_with_invalid_slug(self):
        """
        Tests that dislike article fails for a slug that
        does not exists
        """
        user = self.register_and_loginUser()
        data = {
            'slug': 'this-does-not-exist'
        }
        like_url = reverse('articles:dislike-article', kwargs=data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(like_url)
        self.assertTrue(
            response.data.get('detail'),
            'Article with slug \'this-does-not-exist\' was not found'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_article_by_slug(self):
        """
        Tests that an article can be retrieved using a slug
        """
        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')

        article = self.like_helper_class.get_article_by_slug(
            model=Article,
            slug=response.data.get('slug')
        )
        self.assertEqual(type(article), Article)
