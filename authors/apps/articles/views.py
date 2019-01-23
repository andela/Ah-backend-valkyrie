from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models
from . import serializers
from .renderers import LikeArticleJSONRenderer
from .helper import LikeHelper

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
    lookup_field = 'slug'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        authority.IsOwnerOrReadOnly,
    )


class RetrieveAuthorArticles(generics.ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def get_queryset(self):
        return self.queryset.filter(author_id=self.kwargs.get('pk'))


class LikeArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (LikeArticleJSONRenderer,)
    serializer_class = serializers.LikeArticleSerializer
    like_helper_class = LikeHelper()

    def post(self, request):
        article = None
        slug = request.data.get('slug')
        if slug and len(slug.strip(' ')) > 0:
            article = self.like_helper_class.get_article_by_slug(
                model=models.Article,
                slug=request.data.get('slug')
            )
        data = {
            "article": article.id if article else None,
            "user": request.user.id,
            "like": request.data.get('like')
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=serializer.action_status)
