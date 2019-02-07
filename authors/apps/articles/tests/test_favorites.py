from django.test import TestCase
from  rest_framework.reverse import reverse
from rest_framework import status

from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.articles.helper import FavoriteHelper
from django_currentuser.middleware import get_current_user


class FavoriteTestCase(BaseTestMethods):
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
            "You are not allowed to favorite your own article"
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
    
    def test_is_favorited_method(self):
        #create article
        response =self.favorite_article()
        user = get_current_user().id  
        article_id = self.like_helper_class.get_article_by_slug(
            model=self.model2,
            slug=response.data['article']['slug']
        )
        self.assertEqual(self.favorite.is_favorited(
            model=self.model,
            user_id=user,
            article_id=article_id.id), True)

    def test_is_favorited_false(self):
            #create article
        article =self.create_article()
        user = get_current_user().id  
        article_id = self.like_helper_class.get_article_by_slug(
            model=self.model2,
            slug=article.data['slug']
        )
        self.assertEqual(self.favorite.is_favorited(
            model=self.model,
            user_id=user,
            article_id=article_id.id), False)
    
    def test_favorite_count(self):
        response =self.favorite_article() 
        article_id = self.like_helper_class.get_article_by_slug(
            model=self.model2,
            slug=response.data['article']['slug']
        )
        self.assertEqual(self.favorite.favorite_count(
            model=self.model,
            article_id=article_id.id), True)

    def test_is_favorite_count_false(self):
         #create article
        article =self.create_article()
        user = get_current_user().id  
        article_id = self.like_helper_class.get_article_by_slug(
            model=self.model2,
            slug=article.data['slug']
        )
        self.assertEqual(self.favorite.favorite_count(
            model=self.model,
            article_id=article_id.id), False)

    def test_get_article_by_slug(self):
        #create article
        article =self.create_article()
        response = self.like_helper_class.get_article_by_slug(
            model=self.model2,
            slug=article.data['slug']
        )
        self.assertEqual(response.slug, "test-article-today")
