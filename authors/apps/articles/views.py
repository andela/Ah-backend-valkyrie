from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.renderers import BrowsableAPIRenderer
from django.http import JsonResponse
import json

from . import models
from . import serializers
from .renderers import ArticleJSONRenderer
from authors.apps.core import authority


class ListCreateArticle(generics.ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ArticleSerializer(queryset, many=True)
        return Response({
            "articles": serializer.data,
            "articlesCount": len(serializer.data)
        })


class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = (ArticleJSONRenderer,)

    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    lookup_field = 'slug'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        authority.IsOwnerOrReadOnly,
    )


class RetrieveAuthorArticles(generics.ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        user_id = get_user_model().objects.get(username=username)
        return self.queryset.filter(author_id=user_id)

class ListCreateTag(generics.ListCreateAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.TagSerializer(queryset, many=True)
        return Response({
            "tags": serializer.data
        })


class RetrieveUpdateDestroyTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
