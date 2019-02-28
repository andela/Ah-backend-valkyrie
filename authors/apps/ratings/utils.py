from django.db.models import Avg
# from django_currentuser.middleware import get_current_user


def fetch_rating_average(rating, article_id):
    average_ratings = rating.objects.filter(
        article_id=article_id).values('points').aggregate(Avg('points'))

    if not average_ratings:
        return "Article '{}' has no ratings".format(article_id)
    return average_ratings


def get_user_ratings(**kwargs):
    points = None
    try:
        points = kwargs.get('model').objects.get(article_id=kwargs.get(
            'article_id'), rater_id=kwargs.get('rater_id'))
    except:
        return {
            'points': 0,
            'rater': kwargs.get('rater_id'),
            'article': kwargs.get('article_id')
        }
    return {
        'points': points.points,
        'rater': points.rater_id,
        'article': points.article_id
    }
