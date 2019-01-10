from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('users/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='update-retrieve-user'),
    path('users/', RegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', LoginAPIView.as_view(), name='user-login'),
]
