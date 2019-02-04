from authors.apps.authentication.tests.base import BaseTestMethods
from authors.apps.articles.tests.test_search_article import SearchTestCase
from rest_framework import status

class TestCommentEditHistory(BaseTestMethods):

    def post_comment(self):
        article = self.post_article()
        user = self.register_and_loginUser()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.data['token']
        )
        response = self.client.post(
            '/api/v1/articles/' + article['slug'] +'/comments/',
            data=self.comment, format='json'
        )
        return response.data

    def test_update_and_get_comment_edit_history(self):
        comment = self.post_comment()
        response = self.client.put(
            '/api/v1/articles/test-article-today/comments/' + str(comment['comment']['id']),
            data=self.updated_comment, format='json'
        )
        get_response = self.client.get(
            '/api/v1/articles/test-article-today/comments/' + str(comment['comment']['id']),
            data=self.updated_comment, format='json'
        )
        self.assertEquals(response.data['message'], "Comment updated successfully")
        self.assertEquals(get_response.data['body'], "Updated this test comment.")
        self.assertEquals(get_response.data['comment_history'][0]['body'], "This is a test comment.")

    def test_update_comment_not_found(self):
        comment = self.post_comment()
        response = self.client.put(
            '/api/v1/articles/test-article-today/comments/' + str(comment['comment']['id'] +  1),
            data=self.updated_comment, format='json'
        )
        self.assertEquals(response.data['error'], "Cannot find this comment.")
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_other_user_comment(self):
        comment = self.post_comment()
        user2 = self.register_and_login_user2()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user2.data['token']
        )
        response = self.client.put(
            '/api/v1/articles/test-article-today/comments/' + str(comment['comment']['id']),
            data=self.updated_comment, format='json'
        )
        self.assertEquals(response.data['error'], "No Permission to edit this comment")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
