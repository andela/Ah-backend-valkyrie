

class FavoriteHelper:

    def is_favorited(self, **kwargs):
        try:
            favourite = kwargs.get('model').objects.all().filter(
                article=kwargs.get('article_id')
            ) 
            filtered_favourite = favourite.filter(author=kwargs.get('user_id'))
            if favourite and filtered_favourite:
                return True
            else:
                return False    
        except Exception as e:
            return False

    def favorite_count(self, **kwargs):
        count_favorite = kwargs.get('model').objects.all().filter(
            article=kwargs.get('article_id')
        )
        return len(count_favorite)
        # print(kwargs.get('article_id'))