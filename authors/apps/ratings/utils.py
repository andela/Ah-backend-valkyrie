from django.db.models import Avg


def fetch_rating_average(rating, article_id):
    average_ratings = rating.objects.filter(
        article_id=article_id).values('points').aggregate(Avg('points'))

    if not average_ratings:
        return "Article '{}' has no ratings".format(article_id)
    return average_ratings
