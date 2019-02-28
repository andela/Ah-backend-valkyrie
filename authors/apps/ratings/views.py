from .models import Rating
from .serializers import CreateRatingSerializer, RatingSerializer
from authors.apps.articles.models import Article
from authors.apps.ratings.utils import fetch_rating_average, get_user_ratings

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions, status


# Create your views here.
def fetch_article_helper(slug):
    try:
        article = Article.objects.get(slug=slug)

    except Article.DoesNotExist:
        raise exceptions.NotFound(
            "Article with slug '{}' doesnot exist".format(slug)
        )
    return article


class RatingAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingSerializer

    def post(self, request, slug):
        # Fetch article
        article = fetch_article_helper(slug)
        # check if the logged in user is the article author
        if article.author.id == request.user.id:
            response_message = {
                'message': 'You cannot rate your own article'
            }
            return Response(response_message, status=status.HTTP_403_FORBIDDEN)

        post_data = request.data
        first_rating_data = {
            'points': post_data.get('points'),
            'rater': request.user.id,
            'article': article.id
        }
        # check if a current user has already rated this very article
        try:
            current_rating = Rating.objects.get(
                rater_id=request.user.id, article=article.id)
            # check if the current user is passing the same rating for this article
            # and if so tell them to update
            if (current_rating.points == post_data.get('points')):
                response = {
                    'error': 'You cannot rate the same article with same points.'
                }
                return Response(
                    response,
                    status=status.HTTP_403_FORBIDDEN
                )
            # save the updated rating for the article
            serializer = RatingSerializer(
                current_rating, data=request.data, partial=True
            )
            # lookup, compute and update the average rating field on the current article
            average_rating = fetch_rating_average(Rating, article.id)
            article.avg_rating = average_rating

            # if the current user has never rated the current article
            # then create a new rating for that article
        except Rating.DoesNotExist:
            serializer = CreateRatingSerializer(data=first_rating_data)
            average_rating = fetch_rating_average(Rating, article.id)
            article.avg_rating = average_rating

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_message = {
            'message': 'Article rating successful',
            'rating': serializer.data
        }

        return Response(response_message, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        # Fetch an article
        article = fetch_article_helper(slug)
        average_rating = fetch_rating_average(Rating, article.id)
        response = {
            "slug": article.slug,
            "body": article.body,
            "avg_rating": average_rating.get('points__avg')
        }

        return Response(response, status=status.HTTP_200_OK)
