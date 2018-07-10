from django.urls import path

from .views import (ProfileRetrieveAPIView, ProfileFollowAPIView,
                    ProfileFollowersAPIView, ProfileFollowingAPIView)

urlpatterns = [
    path('users/<int:id>/profile/',
         ProfileRetrieveAPIView.as_view(), name='profile'),
    path('users/<username>/profile/follow',
         ProfileFollowAPIView.as_view(), name='follow-profile'),
    path('users/me/profile/followers',
         ProfileFollowersAPIView.as_view(), name='profile-followers'),
    path('users/me/profile/followings',
         ProfileFollowingAPIView.as_view(), name='followings')

]
