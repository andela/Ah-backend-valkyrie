from rest_framework import serializers
from django.db import models
from django.template.defaultfilters import slugify
from rest_framework import status

from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article, Tag


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

        return tag[0].id

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        return value.tag


class ArticleSerializer(serializers.ModelSerializer):

    author = UserSerializer(required=False)
    tagList = TagRelatedField(many=True, required=False)

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

    def create(self, validated_data):
        tag = validated_data['tagList']
        tagList = validated_data.pop('tagList')
        article = Article.objects.create(**validated_data)
        for tag in tagList:
            tag_obj = Tag.objects.get(id=tag) 
            article.tagList.add(tag_obj)

        return article
