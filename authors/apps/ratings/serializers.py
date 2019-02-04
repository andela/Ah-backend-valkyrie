from rest_framework import serializers

from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'points',)


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'points', 'rater', 'article')
