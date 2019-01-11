from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
<<<<<<< HEAD
    path('users/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
=======
    path('users/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='update-retrieve-user'),
    path('users/', RegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', LoginAPIView.as_view(), name='user-login'),
>>>>>>> 944998530d7a1b73674f4974235c561f3d29e11a
]
