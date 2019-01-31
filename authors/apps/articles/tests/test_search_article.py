from authors.apps.authentication.tests.base import BaseTestMethods
from django.urls import reverse
from rest_framework import status

class SearchTestCase(BaseTestMethods):

    def create_article(self):
        register_and_login = self.register_and_loginUser()
        token = register_and_login.data['token']
        post_article_url = reverse(self.get_post_article_url)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.post(post_article_url, data=self.article, format='json')
    
    def test_search_article_by_key_word(self):
        self.create_article()
        url = "/api/v1/articles/search" + '?search=article'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 1)
        self.assertEquals(response.data['results'][0]['title'], 'Test article today')

    def test_search_article_by_key_word_not_found(self):
        self.create_article()
        url = "/api/v1/articles/search" + '?search=Not+exists'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 0)

    def test_search_article_by_title(self):
        self.create_article()
        url = "/api/v1/articles/search" + '?search=Test+article+today&search_key=title'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 1)

    def test_search_article_by_author(self):
        self.create_article()
        url = "/api/v1/articles/search?search=" + self.user['user']['username'] + "&search_key=author"
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 1)
        self.assertEquals(response.data['results'][0]['title'], 'Test article today')

    def test_search_article_by_author_not_found(self):
        self.create_article()
        url = "/api/v1/articles/search?search=Valkyrie&search_key=author"
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 0)

    def test_search_article_by_tag(self):
        self.create_article()
        url = "/api/v1/articles/search?search=" + self.article['tagList'][0] + "&search_key=tag"
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 1)
        self.assertEquals(response.data['results'][0]['title'], 'Test article today')

    def test_search_article_by_tag_not_found(self):
        self.create_article()
        url = "/api/v1/articles/search?search=Valkyrie&search_key=tag"
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['results']), 0)
