from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework import status
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from django.core.exceptions import ObjectDoesNotExist


from . import models
from .models import Article, FavoriteArticle, BookmarkArticle
from . import serializers
from .renderers import ArticleJSONRenderer
from authors.apps.core import authority
from .search import ArticleFilter


class ListCreateArticle(generics.ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


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

class ListTag(generics.ListAPIView):
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


class FavoriteArticlesView(generics.CreateAPIView):
    queryset = models.FavoriteArticle.objects.all()
    serializer_class = serializers.FavoriteArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        try:
            self.article = Article.objects.get(slug=self.kwargs.get('slug'))
        except:
            message = "Article doesnot exist"
            raise NotFound(
                detail=message, 
                code=status.HTTP_404_NOT_FOUND
            )

        if self.article.author.id == self.request.user.id:
            message = "You are not allowed to favorite your own article"
            raise NotAcceptable(
                detail=message, 
                code=status.HTTP_406_NOT_ACCEPTABLE
            )

        try:
            FavoriteArticle.objects.get(
                author=self.request.user.id, 
                article=self.article.id
            )
        except:
            return serializer.save(author=self.request.user, article_id=self.article.id)  
        
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
            articles = Article.objects.all().filter(slug=self.kwargs.get('slug'))
            if not articles.exists():
                message = "Article doesnot exist"
                raise NotFound(
                    detail=message, 
                    code=status.HTTP_404_NOT_FOUND
                )
            favorites = self.queryset.filter(id=self.kwargs.get('pk'))
            if  not favorites.exists():
                message = "favorite doesnot exist"
                raise NotFound(
                    detail=message, 
                    code=status.HTTP_404_NOT_FOUND
                )    
            slug = self.kwargs.get('slug')
            article = Article.objects.get(slug=slug)
            self.destroy(request, *args, **kwargs)
            return Response(
                {
                    "article": article.title,
                     "slug": article.slug,
                     "status": "unfavorited"
                     
                }
                )


class ArticleSearchListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ArticleSerializer
    filter_class = ArticleFilter
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'description', 'body', 'author__username', 'tagList__tag')

    def get_queryset(self):
        queryset = models.Article.objects.all()
        search_key = self.request.query_params.get('search_key', None)
        search_term = self.request.query_params.get('search', None)
        
        if search_key == 'author':
            queryset = queryset.filter(author__username__icontains=search_term)
        if search_key == 'title':
            queryset = queryset.filter(title__icontains=search_term)
        if search_key == 'tag':
            queryset = queryset.filter(tagList__tag__icontains=search_term)
        return queryset


class BookmarkArticleView(generics.ListCreateAPIView):
    queryset = models.BookmarkArticle.objects.all()
    serializer_class = serializers.BookmarkSerializer
    permission_classes = (
            permissions.IsAuthenticatedOrReadOnly,
            authority.IsOwnerOrReadOnly,
        )
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)  
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        slug=self.kwargs.get('slug')
        article = None
        bookmark = None
        try:
            article = get_object_or_404(Article, slug=slug)
            bookmark = self.queryset.get(
                article=article.id,
                user=self.request.user.id
            )
            
            if bookmark.article_id == article.id:
                print(bookmark.article_id)
                response = {'message': 'You cannot bookmark the same article twice'}
                raise NotAcceptable(detail=response, code=status.HTTP_406_NOT_ACCEPTABLE)
                      
        except ObjectDoesNotExist:
            serializer.save(article=article, user=self.request.user)
        
class UnBookmarkArticleView(generics.DestroyAPIView):
        queryset = models.BookmarkArticle.objects.all()
        serializer_class = serializers.BookmarkSerializer
        permission_classes = (
            permissions.IsAuthenticatedOrReadOnly,
            authority.IsBookmarOwner,
        )

        def delete(self, request, *args, **kwargs):
            slug = self.kwargs.get('slug')
            bookmark_id = self.kwargs.get('pk')
            article = get_object_or_404(Article, slug=slug)
            bookmark = get_object_or_404(self.queryset, id=bookmark_id)    
            self.destroy(request, *args, **kwargs)
            return Response(
                {
                    "article": article.title,
                     "slug": article.slug,
                     "status": "unbookmarked"
                     
                }
            
            )    

class GetBookmarkArticle(generics.RetrieveAPIView):
        queryset = models.BookmarkArticle.objects.all()
        serializer_class = serializers.BookmarkSerializer
        permission_classes = (
            permissions.IsAuthenticated,)  

        def get_queryset(self):
            bookmark_id = self.kwargs.get('pk')
            bookmark = get_object_or_404(self.queryset, id=bookmark_id)
            return self.queryset.filter(id=bookmark_id)    