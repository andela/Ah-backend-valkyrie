#pylint: disable=E1101
from rest_framework import serializers, status
from django.db import models

from authors.apps.authentication.serializers import UserSerializer
from .models import Article, LikeArticle


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
            'likes',
            'dislikes'
        )
        model = Article
        read_only_fields = ('author',)


class LikeArticleSerializer(serializers.ModelSerializer):
    action_status = status.HTTP_201_CREATED

    class Meta:
        model = LikeArticle
        fields = ['article', 'user', 'like', 'modified_at']

    def create(self, validated_data):
        try:
            self.instance = LikeArticle.objects.get(
                article_id=validated_data.get('article'),
                user_id=validated_data.get('user')
            )
        except Exception:
            return LikeArticle.objects.create(**validated_data)
        return self._update_like(validated_data)

    def _update_like(self, validated_date):
        if self.instance.like == validated_date.get('like'):
            self.instance.delete()
            self.action_status = status.HTTP_200_OK
        else:
            self.instance.like = validated_date.get('like')
            self.instance.save()
            self.action_status = status.HTTP_200_OK
        return self.instance
