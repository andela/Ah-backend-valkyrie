from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Profile
from .serializers import ProfileSerializer
from .renderers import (ProfileJSONRenderer,
                        FollowingsJSONRenderer, FollowJSONRenderer)
from .exceptions import ProfileDoesNotExist

from django.core.mail import EmailMessage
from notifications.models import Notification


class ProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, id, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__id=id
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist
        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileFollowAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def post(self, request, username=None):
        follower = request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist
        if follower.pk is followee.pk:
            raise PermissionDenied('You cannot follow yourself.')
        follower.follow(followee)

        # Email notification setup
        subject = 'New Follower'
        message = 'This is your lucky day, {} is now following you'.format(
            follower.user.username)
        # Notification setup
        notification = Notification.objects.create(
            actor=follower.user, recipient=followee.user,
            verb=subject)

        to = followee.user.email
        email = EmailMessage(subject, message, to=[to])
        email.content_subtype = 'html'
        email.send()

        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, username=None):
        follower = self.request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileFollowersAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowJSONRenderer,)
    serializer_class = ProfileSerializer

    def list(self, request):
        follows = self.request.user.profile.followers.all()
        serializer = ProfileSerializer(follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileFollowingAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowingsJSONRenderer,)
    serializer_class = ProfileSerializer

    def list(self, request):
        followings = self.request.user.profile.following.all()
        serializer = ProfileSerializer(followings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
