from django.urls import path

from .views import (ListCreateArticle,
                    RetrieveUpdateDestroyArticle, RetrieveAuthorArticles)

app_name = "articles"
urlpatterns = [
    path('', ListCreateArticle.as_view(), name="articles_list"),
    path('<slug:slug>/', RetrieveUpdateDestroyArticle.as_view(), name="article_detail"),
    path('author/<int:pk>/', RetrieveAuthorArticles.as_view(), name="author_articles"),
]
