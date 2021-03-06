from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from authors.apps.articles.helper import LikeHelper


class Comment(models.Model):
    like_helper = LikeHelper()

    body = models.TextField()
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comments object {}'.format(self.body)

    class Meta:
        ordering = ('createdAt',)

    @property
    def comment_likes(self):
        return self.like_helper.get_comment_likes_or_dislike(
            model=CommentReaction,
            comment_id=self.pk,
            like=True
        )

    @property
    def comment_dislikes(self):
        return self.like_helper.get_comment_likes_or_dislike(
            model=CommentReaction,
            comment_id=self.pk,
            like=False
        )


class CommentReaction(models.Model):
    #  Enables a user to like or dislike a comment
    like = models.BooleanField(default=True)
    comment = models.ForeignKey(
        Comment, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.like


class CommentHistory(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(
        Comment, related_name='comment_history',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ('created_at',)
