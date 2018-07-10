from rest_framework import serializers
from django.db import models

from authors.apps.authentication.serializers import UserSerializer
from .models import Article


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
        )
        model = Article
        read_only_fields = ('author',)
