from django.urls import path

from .views import (ListCreateArticle,
                    RetrieveUpdateDestroyArticle, RetrieveAuthorArticles, FavoriteArticlesView, UnfavoriteArticleView)

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
            'author/<int:pk>/', 
            RetrieveAuthorArticles.as_view(), 
            name="author_articles"
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
