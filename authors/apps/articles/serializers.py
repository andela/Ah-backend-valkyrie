#pylint: disable=E1101
from rest_framework import serializers

from authors.apps.authentication.serializers import UserSerializer
from .models import Tag, Article, LikeArticle


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
        )
        model = Tag


class ArticleSerializer(serializers.ModelSerializer):
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # author = UserSerializer()
    # author_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # author_id = serializers.IntegerField()

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
            'author',
        )
        model = Article
        read_only_fields = ('author',)


class LikeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeArticle
        fields = ['article_id', 'user_id', 'like', 'modified_at']

    def create(self, validated_data):
        try:
            self.instance = LikeArticle.objects.get(
                article_id=validated_data.get('article_id'),
                user_id=validated_data.get('user_id')
            )
        except Exception:
            return LikeArticle.objects.create(**validated_data)
        return self._update_like(validated_data)

    def _update_like(self, validated_date):
        if self.instance.like == validated_date.get('like'):
            self.instance.delete()
        else:
            self.instance.like = validated_date.get('like')
            self.instance.save()
        return self.instance
