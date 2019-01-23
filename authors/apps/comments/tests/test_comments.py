from authors.apps.authentication.tests.base import BaseTestMethods
from rest_framework import status
from django.urls import reverse


class TestComments(BaseTestMethods):

    comment = {
        "comment": {
            "body": "This is another test comment."
        }
    }

    comment2 = {
        "body": "This is another test comment."
    }

    comment3 = {
        "comment": {
            "body": "This is another test comment."
        }
    }

    def get_user_token(self):
        user = self.register_and_loginUser()
        return user.data['token']

    def get_user2_token(self):
        user = self.register_and_login_user2()
        return user.data['token']

    def post_article(self):
        post_article_url = reverse(self.get_post_article_url)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token())
        article = self.client.post(
            post_article_url,data=self.article, format='json')
        return article.data

    def test_posting_a_comment(self):
        # user posting a comment.
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )      
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('This is another test comment.', response.data['comment']['body'])

    def test_posting_a_comment_twice(self):
        # user posting a comment twice.
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/", data=self.comment, format='json')
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/", data=self.comment, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
                "You can't give the same comment twice on the same article",
                    response.data['message'])

    def test_deleting_comment(self):
        # deleting a comment
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response= self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )
        response2 = self.client.delete(
            "/api/v1/articles/" + article['slug'] + "/comments/"
            + str(response.data['comment']['id']), format='json'
        )            
        self.assertEqual(
            response2.status_code, status.HTTP_204_NO_CONTENT)

    def test_updating_a_comment(self):
        # user updating a comment.
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )
        response2 = self.client.put(
            "/api/v1/articles/" + article['slug'] + "/comments/"
            + str(response.data['comment']['id']),
            data=self.comment2, format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual("This is another test comment.", str(
                    response2.data['body']))

    def test_viewing_single_comment(self):
        # user updating a comment.
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/", data=self.comment, format='json')
        response3 = self.client.get(
            "/api/v1/articles/" + article['slug'] + "/comments/"
            + str(response.data['comment']['id'])
        )
        self.assertEqual(
            response3.status_code, status.HTTP_200_OK)
        self.assertIn(
                "This is another test comment.", str(
                    response3.data))                           

    def test_viewing_multiple_comments(self):
        # user updating a comment.
        article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response2 = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )
        response4 = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment3, format='json'
        )
        response3 = self.client.get(
            "/api/v1/articles/" + article['slug'] + "/comments/")
        self.assertEqual( response3.status_code, status.HTTP_200_OK)
        self.assertIn(
                "This is another test comment.", str(response3.data))

    def test_deleting_comment_by_non_owner(self):
        # deleting a comment
        article = article = self.post_article()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user2_token()
        )
        response = self.client.post(
            "/api/v1/articles/" + article['slug'] + "/comments/",
            data=self.comment, format='json'
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_user_token()
        )
        response2 = self.client.delete(
            "/api/v1/articles/" + article['slug'] + "/comments/"
            + str(response.data['comment']['id'])
        )            
        self.assertEqual(
            response2.status_code, status.HTTP_403_FORBIDDEN)
