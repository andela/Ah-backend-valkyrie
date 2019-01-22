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
            'article': response.data.get('id'),
            'like': True
        }
        like_url = reverse('articles:like-article')
        res = self.client.post(like_url, data=data, format='json')
        self.assertTrue(res.data.get('like'), True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
