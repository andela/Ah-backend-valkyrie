from authors.apps.authentication.tests.base import BaseTestMethods
from rest_framework import status
from django.urls import reverse


class TestLikingComments(BaseTestMethods):

    article = {
        "title": "Test article today",
        "description": "Testing article creation",
        "body": "This is a lorem ipsum section."
    }

    comment = {
        "comment": {
            "body": "This is another test comment."
        }
    }

    comment2 = {
            "body": "This is a test comment update."
        }

    comment3 = {
        "comment": {
            "body": "This is another test comment."
        }
     }

    def post_article(self):
        post_article_url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        article = self.client.post(
            post_article_url,data=self.article, format='json')
        return article.data
    
    
    def get_user_token(self):
            user = self.register_and_loginUser()
            return user.data['token']


    def get_user2_token(self):
        user = self.register_and_login_user2()
        return user.data['token']
                

    def test_liking_a_comment(self):
        # deleting a comment
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )
        response2 = self.client.post(
            "/api/v1/articles/" + "comments/"
            + str(response.data['comment']['id'])+"/like", format='json'
        )            
        self.assertEqual(
            response2.status_code, status.HTTP_200_OK)
        self.assertTrue(response2.data["comment_like"]["like"])

    
    def test_unliking_a_comment(self):
        # deleting a comment
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )
        self.client.post(
            "/api/v1/articles/" + "comments/"
            + str(response.data['comment']['id'])+"/like", format='json'
        )            
        response2 = self.client.post(
            "/api/v1/articles/" + "comments/"
            + str(response.data['comment']['id'])+"/like", format='json'
        )           
        self.assertEqual(
            response2.status_code, status.HTTP_200_OK)
        self.assertIn("comment disliked", response2.data["message"])
