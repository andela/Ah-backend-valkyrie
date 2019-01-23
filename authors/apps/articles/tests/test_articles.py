from django.test import TestCase
from  rest_framework.reverse import reverse
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
        author_id = request.data['author']
        author_articles = reverse(self.get_author_articles, args=[author_id])
        request = self.client.get(author_articles)
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.data), 0)
        self.assertEqual(request.data['results'][0]['author'], author_id)

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
        self.assertEqual(request.data['slug'], "test-article-today-2")

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
    # test favorite article 
    def test_favorite_article(self):
        #create an article
        response = self.create_article()
        article_slug = response.data['slug']
        #user favorites an article
        url  = reverse("articles:favorite-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['article']['slug'], 
            "test-article-today"
        )

        #test user cannot favorite his/her own article  
    def test_user_cannot_favorite_own_article(self):
        #create article
        response = self.create_article()
        article_slug = response.data['slug']
        #favorite your article
        url  = reverse("articles:favorite-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token()
        )
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data['detail'], 
            "You're not authorised to favorite your own artcle"
        ) 

    def test_user_cannot_favorite_article_again(self):
        #create article
        response = self.create_article()
        article_slug = response.data['slug']
        #user favorites article
        url  = reverse("articles:favorite-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       
        # user favorites article again
        url  = reverse("articles:favorite-articles", args=[article_slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data['detail'], 
            "Article already favorited by you"
        )
    def test_user_cannnot_favorite_non_existant_article(self):
        # create article
        self.create_article()

        #  user favorite article with a wrong slug
        slug = "today-comes-tomorrow"
        url = reverse("articles:favorite-articles", args=[slug])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Article doesnot exist") 

    def test_unfavorite_article(self):
        # favorite an article
        response = self.favorite_article()
        favorite_id = response.data['id']
        article_slug = self.create_article().data['slug']

        #Unfavorite an article
        url  = reverse(
            "articles:unfavorite-articles", 
            args=[article_slug, favorite_id]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],"unfavorited")

    def test_user_cannnot_unfavorite_non_existant_article(self):
        # Favorite article
        response = self.favorite_article()
        favorite_id = response.data['id']
        
        #  user unfavorites article with a wrong slug
        slug = "today-comes-tomorrow"
        url = reverse("articles:unfavorite-articles", args=[slug, favorite_id])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Article doesnot exist")
    
            
    def test_user_cannnot_unfavorite_non_existant_favorite(self):
        # favorite article
        self.favorite_article()
        article_slug = self.create_article().data['slug']       
        #  user unfavorites article with a wrong slug
        favorite = 10
        url = reverse("articles:unfavorite-articles", args=[article_slug, favorite])
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "favorite doesnot exist")
    
