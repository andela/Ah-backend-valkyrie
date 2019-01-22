from rest_framework import serializers
from django.db import models
from django.template.defaultfilters import slugify
from rest_framework import status

from authors.apps.authentication.serializers import UserSerializer
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Tag
        fields = ('name',)

class TagRelatedField(serializers.RelatedField):

    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        name, created = Tag.objects.get_or_create(name=data, slug=slugify(data))

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        return value.name


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
