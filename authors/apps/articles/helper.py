
from django.contrib.auth import get_user_model


class LikeHelper:

    def get_likes_or_dislike(self, **kwargs):
        likes = kwargs.get('model').objects.all().filter(
            like=kwargs.get('like')
        )
        filtered_list = likes.filter(article_id=kwargs.get('article_id'))
        return {
            'users': self._get_usernames(filtered_list),
            'count': filtered_list.count()
        }

    def _get_usernames(self, filtered_list):
        """
        Retrieves a list of users who liked or disliked a
        particular article
        """

        usernames = []
        for like in filtered_list:
            usernames.append(
                get_user_model().objects.get(pk=like.user.id).username
            )
        return usernames

    def get_article_by_slug(self, **kwargs):
        """Retrieves a user using the unique slug"""

        article = kwargs.get('model').objects.get(slug=kwargs.get('slug'))
        return article
