import readtime
import json
from rest_framework import serializers, status
from django.db import models
from django.template.defaultfilters import slugify
from rest_framework import status

from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer
from .models import (
    Article,
    Tag,
    FavoriteArticle,
    BookmarkArticle,
    ReadingStats,
    HighlightedText,
    LikeArticle
)
from ..comments.serializers import CommentSerializer


class TagSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.tag

    class Meta:
        model = Tag
        fields = ('tag',)


class TagRelatedField(serializers.RelatedField):

    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        tag = Tag.objects.get_or_create(tag=data, slug=slugify(data))

        return tag[0]

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        return value.tag

class ArticleImageRelatedField(serializers.RelatedField):

    def get_queryset(self):
        return BlogImage.objects.all()

    def to_internal_value(self, data):
        image = BlogImage.objects.create(image=data)

        return image[0]

    def to_representation(self, value):
        return value.image


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    tagList = TagRelatedField(many=True, required=False)
    read_time = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'slug',
            'title',
            'description',
            'body',
            'tagList',
            'average_rating',
            'createdAt',
            'updatedAt',
            'author',
            'likes',
            'dislikes',
            'favorited',
            'favorites_count',
            'read_time',
            'comments',
            'read_count',
        )
        model = Article
        read_only_fields = ('author', 'comments')

    def create(self, validated_data):
        try:
            tagList = validated_data.pop('tagList')
            article = Article.objects.create(**validated_data)
            for tag in tagList:
                tag_obj = Tag.objects.get(id=tag.id)
                article.tagList.add(tag_obj)

            return article
        except KeyError as identifier:
            raise serializers.ValidationError({
                'tagList': 'Please provide a list of tags'
            })

    def get_read_time(self, instance):
        post = instance.body
        return str(readtime.of_text(post))


class LikeArticleSerializer(serializers.ModelSerializer):

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
        else:
            self.instance.like = validated_date.get('like')
            self.instance.save()
        return self.instance


class FavoriteArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)

    class Meta:
        fields = (
            'id',
            'article',
        )
        model = FavoriteArticle


class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)

    class Meta:
        fields = (
            'id',
            'article',
            )
        model = BookmarkArticle



class ReadingStatSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)
    class Meta:
        fields = (
            'article',
            'read_on',
        )
        model = ReadingStats
        article = ArticleSerializer(required=False)
        class Meta:
            fields = (
                'id' ,
                'article',
            )
            model = FavoriteArticle

class HighlightSerializer(serializers.ModelSerializer):
        author = UserSerializer(required=False)
        class Meta:
            fields = (
                'id' ,
                'author',
                'startIndex',
                'endIndex',
                'created',
                'selected_text',
                'comment',
            )
            model = HighlightedText

        def create(self, validated_data):
            try:
                article_slug = self.context["slug"]
            except KeyError as e:
                raise serializers.ValidationError({
	                'slug': 'Please provide a slug'
	            })

            article_id = validated_data.pop('article')
            article = Article.objects.get(slug=article_slug)
            article_text = article.body
            startIndex = int(validated_data.pop('startIndex'))
            endIndex = int(validated_data.pop('endIndex'))

            # reassign values if endIndex is greater
            if startIndex > endIndex:
                print(startIndex)
                temp_startIndex = startIndex
                temp_endIndex = endIndex

                startIndex = temp_endIndex
                endIndex = temp_startIndex

            validated_data['startIndex'] = startIndex
            validated_data['endIndex'] = endIndex
            validated_data['article'] = article

            selectedText = article_text[startIndex:endIndex]
            if selectedText == "":
                raise serializers.ValidationError({
	                'highlight': 'Not a valid highlight'
	            })

            highlight = HighlightedText.objects.create(**validated_data)
            return highlight
