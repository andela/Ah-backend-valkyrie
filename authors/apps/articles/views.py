from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, NotAcceptable
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from authors.apps.profiles.models import Profile
from django_social_share.templatetags import social_share

from . import models
from .models import Article, FavoriteArticle, BookmarkArticle, ReportArticle
from . import serializers
from .helper import LikeHelper, ReportArticleHelper
from .renderers import ArticleJSONRenderer
from authors.apps.core import authority
from .search import ArticleFilter
from authors.apps.articles.pagination import ArticlePagination
from django_filters import rest_framework as filter


class ListCreateArticle(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = ArticlePagination

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

    def initial(self, request, *args, **kwargs):
        """
        Track reading stats
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)
        article = Article.objects.get(slug=self.kwargs.get('slug'))
        author = self.request.user
        if not request.user.is_anonymous:
            read = models.ReadingStats.objects.update_or_create(
                article=article,
                author=self.request.user
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


class LikeArticleAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeArticleSerializer
    like_helper_class = LikeHelper()

    def post(self, request, **kwargs):
        article = self.like_helper_class.get_article_by_slug(
            model=models.Article,
            slug=kwargs.get('slug')
        )

        data = {
            "article": article.id if article else None,
            "user": request.user.id,
            "like": True
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class DislikeArticleAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeArticleSerializer
    like_helper_class = LikeHelper()

    def post(self, request, **kwargs):
        article = self.like_helper_class.get_article_by_slug(
            model=models.Article,
            slug=kwargs.get('slug')
        )

        data = {
            "article": article.id if article else None,
            "user": request.user.id,
            "like": False
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if not favorites.exists():
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


class ShareArticleView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        provider = kwargs.get('provider')
        slug = kwargs.get('slug')
        providers = ['facebook', 'email', 'twitter']

        if provider not in providers:
            return Response(
                {'error': 'Invalid provider link'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            return Response({"message": "This article doesnot exist."},
                            status=status.HTTP_404_NOT_FOUND)

        article_link = request.build_absolute_uri(
            '/articles/{}/'.format(article.slug))

        context = {'request': request}
        user = Profile.objects.get(user=article.author_id)

        subject = '{0} shared {1} with you.'.format(
            user.first_name, article.title)

        text = 'Read {0} shared by {1} {2}'.format(
            article.title, user.first_name, user.last_name)

        if provider == 'email':
            link = social_share.send_email_url(
                context, subject, text, article_link)['mailto_url']
            return Response(
                {
                    'link': link,
                    'provider': provider
                },
                status=status.HTTP_200_OK)
        return Response(
            {
                'link': self.set_social_links(
                    context, provider, article_link, args
                ), 'provider': provider
            }, status=status.HTTP_200_OK)

    def set_social_links(self, context, provider, link, *args):

        providers = {
            'twitter': [social_share.post_to_twitter_url, 'tweet_url'],
            'facebook': [social_share.post_to_facebook_url, 'facebook_url']
        }
        provider_link = providers.get(provider, providers['facebook'])

        return provider_link[0](context, link)[provider_link[1]]


class ReportArticleAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ReportArticleSerializer
    like_helper_class = LikeHelper()
    report_article_helper = ReportArticleHelper()

    def post(self, request, **kwargs):
        article = self.like_helper_class.get_article_by_slug(
            model=Article,
            slug=kwargs.get('slug')
        )
        if request.user.id == article.author.id:
            msg = 'You cannot report your own article'
            raise NotAcceptable(
                detail=msg, code=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "article": article.id if article else None,
            "user": request.user.id,
            "message": request.data.get('message')
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None, **kwargs):
        if request.user.is_superuser:
            if kwargs.get('slug'):
                #  Get all reports for a single article
                article = self.like_helper_class.get_article_by_slug(
                    model=Article,
                    slug=kwargs.get('slug')
                )
                reported = self.report_article_helper.get_reports_for_single_article(
                    model=ReportArticle,
                    article=article
                )
            else:
                #  Get all reports for all articles
                reported = self.report_article_helper.get_all_reports(
                    model=ReportArticle
                )
            serializer = serializers.ReportArticleSerializer(
                reported, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        msg = 'You are not authorized to access this resource'
        return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)


class ArticleSearchListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ArticleSerializer
    filter_class = ArticleFilter
    filter_backends = (filter.DjangoFilterBackend, SearchFilter, )
    search_fields = (
        'title',
        'description',
        'body',
        'author__username',
        'tagList__tag'
    )

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
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
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
                response = {
                    'message': 'You cannot bookmark the same article twice'}
                raise NotAcceptable(
                    detail=response, code=status.HTTP_406_NOT_ACCEPTABLE)

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


class ReadingStatsView(generics.ListAPIView):
    queryset = models.ReadingStats.objects.all()
    serializer_class = serializers.ReadingStatSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        authority.IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class HighlightListCreate(generics.ListCreateAPIView):
    queryset = models.HighlightedText.objects.all()
    serializer_class = serializers.HighlightSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    lookup_field = 'slug'

    def perform_create(self, serializer):
        article = Article.objects.get(slug=self.kwargs.get('slug'))
        return serializer.save(article=article, author=self.request.user)

    def get_serializer_context(self):
        return {"slug": self.kwargs['slug']}
