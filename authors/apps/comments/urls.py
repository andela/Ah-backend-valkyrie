from django.urls import path
from .api_views import CommentList, CommentDetail, CommentDislike, CommentLike

urlpatterns = [
    path('<slug:slug>/comments/', CommentList.as_view()),
    path('<slug:slug>/comments/<int:pk>', CommentDetail.as_view()),
    path('comments/<int:pk>/like', CommentLike.as_view()),
    path('comments/<int:pk>/dislike', CommentDislike.as_view())
]