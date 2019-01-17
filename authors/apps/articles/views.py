from rest_framework import generics, permissions

from . import models
from . import serializers
from authors.apps.core import authority

class ListCreateArticle(generics.ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        authority.IsOwnerOrReadOnly,
    )

class RetrieveArticleWithSlug(generics.RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    lookup_field = 'slug'


class ListCreateTag(generics.ListCreateAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class RetrieveUpdateDestroyTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
