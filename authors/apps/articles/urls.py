from django.urls import path

from .views import (
    ListCreateArticle, ListCreateTag, RetrieveUpdateDestroyArticle,
    LikeArticleAPIView
)

app_name = "articles"
urlpatterns = [
    path('', ListCreateArticle.as_view(), name="articles_list"),
    path('<int:pk>/', RetrieveUpdateDestroyArticle.as_view(), name="article_detail"),
    path('tags', ListCreateTag.as_view(), name="tags_list"),
    path('tags/<int:pk>/', RetrieveUpdateDestroyArticle.as_view(), name="tag_detail"),
    path('like/', LikeArticleAPIView.as_view(), name='like-article')
]
