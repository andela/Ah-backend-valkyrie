from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView,
    UserRetrieveUpdateAPIView,
    UserPasswordResetRequestAPIView,
    UserPasswordResetConfirmAPIView,
    UserAccountVerificationAPIView
)

urlpatterns = [
    path(
        'users/<int:pk>/',
        UserRetrieveUpdateAPIView.as_view(),
        name='update-retrieve-user'),
    path(
        'users/',
        RegistrationAPIView.as_view(),
        name='user-registration'),
    path(
        'users/login/',
        LoginAPIView.as_view(),
        name='user-login'),

    # User reset passord urls
    path(
        'users/reset_password',
        UserPasswordResetRequestAPIView.as_view(),
        name='reset_password'),
    path(
        'users/reset_password_confirm/<str:token>',
        UserPasswordResetConfirmAPIView.as_view(),
        name='reset_password_confirm'),
    path(
        'users/verify-account/<str:token>/<str:email>',
        UserAccountVerificationAPIView.as_view(),
        name='user-account-verification'
    ),
]
