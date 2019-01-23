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
            'slug': response.data.get('slug'),
            'like': True
        }
        like_url = reverse('articles:like-article')
        res = self.client.post(like_url, data=data, format='json')
        self.assertTrue(res.data.get('like'), True)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_unlike_article(self):
        """Tests that a like is removed from an article"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug'),
            'like': True
        }
        like_url = reverse('articles:like-article')
        self.client.post(like_url, data=data, format='json')
        #  Like same article a second time
        res = self.client.post(like_url, data=data, format='json')
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
            'slug': response.data.get('slug'),
            'like': False
        }
        like_url = reverse('articles:like-article')
        res = self.client.post(like_url, data=data, format='json')
        self.assertFalse(res.data.get('like'), False)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_un_dislike_article(self):
        """Tests that a dislike is removed from an article"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug'),
            'like': False
        }
        like_url = reverse('articles:like-article')
        self.client.post(like_url, data=data, format='json')
        #  Dislike same article a second time
        res = self.client.post(like_url, data=data, format='json')
        self.assertFalse(res.data.get('like'), False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_like_article_without_article_field(self):
        """Tests that like or dislike article requires the slug field"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        self.client.post(url, data=self.article, format='json')
        data = {
            'like': False
        }
        like_url = reverse('articles:like-article')
        res = self.client.post(like_url, data=data, format='json')
        self.assertEqual(
            json.loads(res.content.decode()).get('slug'),
            'slug is a required field'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_article_without_like_field(self):
        """Tests that like or dislike article requires the like field"""

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        data = {
            'slug': response.data.get('slug')
        }
        like_url = reverse('articles:like-article')
        res = self.client.post(like_url, data=data, format='json')
        self.assertEqual(
            json.loads(res.content.decode()).get('like'),
            'like is a required field'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_article_without_input_data(self):
        """
        Tests that like or dislike article requires both
        article field and like field
        """

        user = self.register_and_loginUser()
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data.get('token'))
        response = self.client.post(url, data=self.article, format='json')
        like_url = reverse('articles:like-article')
        res = self.client.post(like_url, format='json')
        self.assertEqual(
            json.loads(res.content.decode()).get('like'),
            'like is a required field'
        )
        self.assertEqual(
            json.loads(res.content.decode()).get('slug'),
            'slug is a required field'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

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
            'slug': response.data.get('slug'),
            'like': True
        }
        like_url = reverse('articles:like-article')
        self.client.post(like_url, data=data, format='json')
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
            'slug': response.data.get('slug'),
            'like': False
        }
        like_url = reverse('articles:like-article')
        self.client.post(like_url, data=data, format='json')
        article = self.like_helper_class.get_article_by_slug(
            model=Article,
            slug=response.data.get('slug')
        )
        likes = self.like_helper_class.get_likes_or_dislike(
            model=LikeArticle,
            like=False,
            article_id=article.id
        )
        self.assertEqual(likes.get('count'), 1)
