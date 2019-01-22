from rest_framework import serializers
from django.db import models

from authors.apps.authentication.serializers import UserSerializer
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True, many=False)

    class Meta:
        fields = (
            'name',
        )
        model = Tag


class ArticleSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )
    author = UserSerializer()
    # tagList = Article.get_tag_names
    # tagList = Article.get_tag_names
    tagList = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = (
            'slug',
            'title',
            'description',
            'body',
            'tagList',
            'createdAt',
            'updatedAt',
            'author',
        )
        model = Article
        read_only_fields = ('author',)
