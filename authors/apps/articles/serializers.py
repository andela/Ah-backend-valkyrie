from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import models

from authors.apps.authentication.serializers import UserSerializer
from .models import Tag, Article

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
        )
        model = Tag

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
            'tagList',
            'createdAt',
            'updatedAt',
            'author',
        )
        model = Article
        read_only_fields = ('author',)
