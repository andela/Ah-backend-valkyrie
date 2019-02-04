from rest_framework import status
from rest_framework.reverse import reverse

# from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.ratings.tests.base import RatingBaseData
from authors.apps.authentication.models import User


class TestUserRating(BaseTestMethods, RatingBaseData):
    def test_successful_article_rating(self):
        user_1 = self.register_and_loginUser()

        token = user_1.data.get('token')
        article = self.article
        # create an article
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        response = self.client.post(url, data=article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # another registered user should be able to rate another authors article
        user_2 = self.register_and_login_user2()
        token = user_2.data.get('token')
        data = self.rating
        url = reverse('rating', kwargs={
                      'slug': response.data['slug']})
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        rating_response = self.client.post(url, data=data, format='json')
        self.assertEqual(rating_response.status_code, status.HTTP_201_CREATED)

    def test_article_author_cant_rate_their_own_article(self):
        user_1 = self.register_and_loginUser()
        token = user_1.data.get('token')
        article = self.article

        # create an article
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        response = self.client.post(url, data=article, format='json')

        # Try to rate your own article
        data = self.rating
        url = reverse('rating', kwargs={
                      'slug': response.data['slug']})
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        rating_response = self.client.post(url, data=data, format='json')
        self.assertEqual(rating_response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_cant_rate_the_same_article_twice_with_same_rating(self):
        user_1 = self.register_and_loginUser()

        token = user_1.data.get('token')
        article = self.article
        # create an article
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        response = self.client.post(url, data=article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # another registered user should be able to rate the article
        user_2 = self.register_and_login_user2()
        token = user_2.data.get('token')
        data = self.rating
        url = reverse('rating', kwargs={
                      'slug': response.data['slug']})
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        rating_response_1 = self.client.post(url, data=data, format='json')

        # rate the same article the second time with the same rating
        rating_response_2 = self.client.post(url, data=data, format='json')
        self.assertEqual(rating_response_2.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_fetch_article_rating(self):
        user_1 = self.register_and_loginUser()

        token = user_1.data.get('token')
        article = self.article
        # create an article
        url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        response = self.client.post(url, data=article, format='json')

        # fetch an article that matches the slug
        url = reverse('rating', kwargs={
                      'slug': response.data['slug']})
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        article_response = self.client.get(url, format='json')
        self.assertEqual(article_response.status_code,
                         status.HTTP_200_OK)
