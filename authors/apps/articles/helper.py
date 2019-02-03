from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from rest_framework import status


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
        if kwargs.get('slug') and len(kwargs.get('slug').strip(' ')) > 0:
            try:
                self.article = kwargs.get('model').objects.get(
                    slug=kwargs.get('slug')
                )
            except:
                msg = 'Article with slug \'{}\' was not found'.format(
                    kwargs.get('slug')
                )
                raise NotFound(detail=msg, code=status.HTTP_404_NOT_FOUND)

        return self.article


class StatsHelper:

    def read_count(self, **kwargs):
        count_reads = kwargs.get('model').objects.all().filter(
            article=kwargs.get('article_id')
        )
        return len(count_reads)


class FavoriteHelper:

    def is_favorited(self, **kwargs):
        favourite = kwargs.get('model').objects.all().filter(
            article=kwargs.get('article_id')
        )
        filtered_favourite = favourite.filter(author=kwargs.get('user_id'))
        if len(filtered_favourite) > 0:
            return True
        return False

    def favorite_count(self, **kwargs):
        count_favorite = kwargs.get('model').objects.all().filter(
            article=kwargs.get('article_id')
        )
        return len(count_favorite)
