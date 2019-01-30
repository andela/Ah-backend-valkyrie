import readtime
import json
from rest_framework import serializers
from django.db import models
from django.template.defaultfilters import slugify
from rest_framework import status

from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article, Tag, FavoriteArticle


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


class ArticleSerializer(serializers.ModelSerializer):

    author = UserSerializer(required=False)
    tagList = TagRelatedField(many=True, required=False)
    read_time = serializers.SerializerMethodField()

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
            'favorited',
            'favorites_count',
            'read_time'
        )
        model = Article
        read_only_fields = ('author',)

    def create(self, validated_data):
        tagList = validated_data.pop('tagList')
        article = Article.objects.create(**validated_data)
        for tag in tagList:
            tag_obj = Tag.objects.get(id=tag.id)
            article.tagList.add(tag_obj)

        return article

    def get_read_time(self, instance):
        post = instance.body
        return str(readtime.of_text(post))


class FavoriteArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)

    class Meta:
        fields = (
            'id',
            'article',
        )
        model = FavoriteArticle
