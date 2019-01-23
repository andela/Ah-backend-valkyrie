from django.urls import path

from .views import ProfileRetrieveAPIView

urlpatterns = [
    path('users/<int:id>/profile/',
         ProfileRetrieveAPIView.as_view(), name='profile'),
]
