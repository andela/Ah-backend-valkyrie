from django.urls import path

from .views import (ListCreateArticle,
                    RetrieveUpdateDestroyArticle, RetrieveAuthorArticles,
                    ListTag)

app_name = "articles"
urlpatterns = [
    path('', ListCreateArticle.as_view(), name="articles_list"),
    path('<slug:slug>/', RetrieveUpdateDestroyArticle.as_view(), name="article_detail"),
    path('author/<str:username>/', RetrieveAuthorArticles.as_view(), name="author_articles"),
    path('tags', ListTag.as_view(), name="tags_list"),
]
