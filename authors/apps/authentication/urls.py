from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, 
    UserAccountVerificationAPIView
)

urlpatterns = [
    path(
        'users/<int:pk>/', 
        UserRetrieveUpdateAPIView.as_view(), 
        name='update-retrieve-user'
    ),
    path(
        'users/', 
        RegistrationAPIView.as_view(), 
        name='user-registration'),
    path(
        'users/login/', 
        LoginAPIView.as_view(), 
        name='user-login'
    ),
    path(
        'users/verify-account/<str:token>/<str:email>', 
        UserAccountVerificationAPIView.as_view(), 
        name='user-account-verification'
    ),
]
