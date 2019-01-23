from rest_framework import serializers
from django.db import models

from authors.apps.authentication.serializers import UserSerializer
from django.http import Http404
from .models import Article, FavoriteArticle


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'slug',
            'title',
            'description',
            'body',
            'createdAt',
            'updatedAt',
            'author',
            'favorited',
            'favorites_count',
        )
        model = Article
        read_only_fields = ('author',)


class FavoriteArticleSerializer(serializers.ModelSerializer):
        article = ArticleSerializer(required=False)
        class Meta:
            fields = ( 
            'id' ,     
            'article',
            )
            model = FavoriteArticle
