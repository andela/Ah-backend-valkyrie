from django.test import TestCase
from  rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

class BookmarkTestCase(BaseTestMethods):

    def test_bookmark_article(self):
        # bookmark article
        response = self.bookmark_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        self.assertEqual(response.data['article']['slug'], "test-article-today")

    def test_bookmark_article_with_wrong_slug(self):
        # create article
        self.create_article()
        article_slug = "whatsup"
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(url, data=self.article, format='json')  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND )
        self.assertEqual(response.data['detail'], "Not found.")

    def test_user_cannot_bookmark_again(self):
        # create article
        article = self.create_article()
        article_slug = article.data['slug']
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(url, data=self.article, format='json')    
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(url, data=self.article, format='json')  
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE )
        self.assertEqual(response.data['message'], "You cannot bookmark the same article twice")

    def test_unbookmark_article(self):
        # bookmark article
        response = self.bookmark_article()
        bookmark_id = response.data['id']
        article_slug = self.create_article().data['slug'] 

        #  unbookmark article
        url = reverse("articles:unbookmark-articles", args=[article_slug, bookmark_id ])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.delete(url, data=self.article, format='json')   
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data.get('status'), "unbookmarked")


    def test_unbookmark_not_existant_bookmark(self):
        # bookmark article
        self.bookmark_article()
        bookmark_id = 10
        article_slug = self.create_article().data['slug'] 

        # unbookmark article
        url = reverse("articles:unbookmark-articles", args=[article_slug, bookmark_id ])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.delete(url, data=self.article, format='json')   
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND )
        
    
    def test_unbookmark_not_existant_article(self):
        # bookmark article
        response = self.bookmark_article()
        bookmark_id = response.data['id']
        article_slug = "whatsup" 

        # unbookmark article
        url = reverse("articles:unbookmark-articles", args=[article_slug, bookmark_id ])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.delete(url, data=self.article, format='json')   
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND )
        self.assertEqual(response.data['detail'], "Not found.")

    def test_get_bookmarks(self):
        article = self.create_article()
        article_slug = article.data['slug']
        # bookmark article 
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(url, data=self.article, format='json') 
        # get article   
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.get(url, data=self.article, format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data['results'][0]['article']['slug'], "test-article-today")

    def test_get_bookmark(self):
        article = self.create_article()
        article_slug = article.data['slug']
        # bookmark article 
        url = reverse("articles:bookmark-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        response = self.client.post(url, data=self.article, format='json') 
        bookmark_id = response.data['id']
        # get article   
        url = reverse("articles:get-bookmark-articles", args=[bookmark_id])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())    
        response = self.client.get(url, data=self.article, format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data['article']['slug'], "test-article-today")    