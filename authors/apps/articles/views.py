from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from django.http import Http404

from . import models
from .models import Article, FavoriteArticle
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


class FavoriteArticlesView(generics.CreateAPIView):
    queryset = models.FavoriteArticle.objects.all()
    serializer_class = serializers.FavoriteArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        authority.IsOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        article = Article.objects.get(slug=self.kwargs.get('slug'))
        if article.author.id == self.request.user.id:
            message = "You're not authorised to favorite your own artcle"
            raise NotAcceptable(
                detail=message, 
                code=status.HTTP_406_NOT_ACCEPTABLE
            )
        favor = None
        try:
            favor = FavoriteArticle.objects.get(
                author=self.request.user.id, 
                article=article.id
            )
        except:
            serializer.save(author=self.request.user, article_id = article.id)
            
        if favor:
            message = "Article already favorited by you"
            raise NotAcceptable(
                detail=message, 
                code=status.HTTP_401_UNAUTHORIZED
            )
                 
            
class UnfavoriteArticleView(generics.DestroyAPIView):
        queryset = models.FavoriteArticle.objects.all()
        serializer_class = serializers.FavoriteArticleSerializer
        permission_classes = (
            permissions.IsAuthenticatedOrReadOnly,
            authority.IsOwnerOrReadOnly,
        )

        def delete(self, request, *args, **kwargs):
            slug = self.kwargs.get('slug')
            article = Article.objects.get(slug=slug)
            return Response(
                {
                    "article": article.title,
                     "slug": article.slug,
                     "status": "unfavorited"
                     
                }
                )
