from django.urls import path

from .views import (
<<<<<<< HEAD
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, 
    UserAccountVerificationAPIView
=======
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    UserAccountVerificationAPIView,UsersListAPIView
>>>>>>> 8ae1661... feat(authentication) Add list users functionality 
)

urlpatterns = [
    path(
        'users/<int:pk>/', 
        UserRetrieveUpdateAPIView.as_view(), 
        name='update-retrieve-user'
    ),
    path(
<<<<<<< HEAD
        'users/', 
=======
        'users/register', 
>>>>>>> 8ae1661... feat(authentication) Add list users functionality 
        RegistrationAPIView.as_view(), 
        name='user-registration'),
    path(
        'users/login/', 
        LoginAPIView.as_view(), 
        name='user-login'
    ),
    path(
<<<<<<< HEAD
=======
        'users/', 
        UsersListAPIView.as_view(), 
        name='list-users-functionality'),
    path(
>>>>>>> 8ae1661... feat(authentication) Add list users functionality 
        'users/verify-account/<str:token>/<str:email>', 
        UserAccountVerificationAPIView.as_view(), 
        name='user-account-verification'
    ),
]
