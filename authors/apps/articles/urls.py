from django.urls import path

from .views import (
    ListCreateArticle,
    RetrieveUpdateDestroyArticle,
    RetrieveAuthorArticles,
    ListTag,
    FavoriteArticlesView,
    UnfavoriteArticleView,
)


app_name = "articles"
urlpatterns = [
    path(
        '',
        ListCreateArticle.as_view(),
        name="articles_list"
    ),
    path(
        '<slug:slug>/',
        RetrieveUpdateDestroyArticle.as_view(),
        name="article_detail"
    ),
    path(
        'author/<str:username>/',
        RetrieveAuthorArticles.as_view(),
        name="author_articles"
    ),
    path(
        'tags',
        ListTag.as_view(),
        name="tags_list"
    ),
    path(
            '<slug:slug>/favorite', 
            FavoriteArticlesView.as_view(), 
            name="favorite-articles"
        ), 
    path(
            '<slug:slug>/favorite/<int:pk>/', 
            UnfavoriteArticleView.as_view(), 
            name="unfavorite-articles"
        )
]
