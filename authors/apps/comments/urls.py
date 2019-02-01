from django.urls import path
from .api_views import CommentList, CommentDetail

urlpatterns = [
    path('<slug:slug>/comments/', CommentList.as_view()),
    path('<slug:slug>/comments/<int:pk>', CommentDetail.as_view()),
]