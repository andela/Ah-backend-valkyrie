from django.urls import path

from .views import (ListCreateArticle,
                    RetrieveUpdateDestroyArticle, RetrieveAuthorArticles,
                    ListCreateTag, RetrieveUpdateDestroyTag)

app_name = "articles"
urlpatterns = [
    path('', ListCreateArticle.as_view(), name="articles_list"),
    path('<slug:slug>/', RetrieveUpdateDestroyArticle.as_view(), name="article_detail"),
    path('author/<int:pk>/', RetrieveAuthorArticles.as_view(), name="author_articles"),
    path('tags', ListCreateTag.as_view(), name="tags_list"),
    path('tags/<int:pk>/', RetrieveUpdateDestroyTag.as_view(), name="tag_detail"),
]
