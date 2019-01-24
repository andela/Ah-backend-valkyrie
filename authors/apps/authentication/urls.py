from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    UserAccountVerificationAPIView
    UserAccountVerificationAPIView,UsersListAPIView
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, 
    UserAccountVerificationAPIView
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    UserAccountVerificationAPIView,UsersListAPIView
)

urlpatterns = [
    path(
        'users/<int:pk>/',
        UserRetrieveUpdateAPIView.as_view(),
        name='update-retrieve-user'
    ),
    path(
        'users/register',
        RegistrationAPIView.as_view(),
        'users/register', 
        'users/', 
        'users/register', 
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
        'users/', 
        UsersListAPIView.as_view(), 
        name='list-users-functionality'),
    path(
        'users/verify-account/<str:token>/<str:email>', 
        UserAccountVerificationAPIView.as_view(), 
        name='user-account-verification'
    ),
]
