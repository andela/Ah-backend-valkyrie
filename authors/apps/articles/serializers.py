from rest_framework import serializers

from .models import Tag, Article

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
        )
        model = Tag

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'slug',
            'title',
            'description',
            'body',
            'tagList',
            'createdAt',
            'updatedAt',
            'favorited',
            'favoritesCount',
            'author'
        )
        model = Article
