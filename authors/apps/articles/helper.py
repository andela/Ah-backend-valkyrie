from rest_framework.exceptions import NotFound
from rest_framework import status

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
  
    def get_article_by_slug(self, **kwargs):
        article = None
        if kwargs.get('slug') and len(kwargs.get('slug').strip(' ')) > 0:
            try:
                article = kwargs.get('model').objects.get(
                    slug=kwargs.get('slug')
                )
            except:
                msg = 'Article with slug \'{}\' was not found'.format(
                    kwargs.get('slug')
                )
                raise NotFound(detail=msg, code=status.HTTP_404_NOT_FOUND)

        return article    


class StatsHelper:

    def read_count(self, **kwargs):
        count_reads = kwargs.get('model').objects.all().filter(
            article=kwargs.get('article_id')
        )
        return len(count_reads)
