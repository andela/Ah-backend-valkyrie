import json

from notifications.models import Notification
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authors.apps.notify.helper import Notifier
from authors.apps.notify.models import MailList
from authors.apps.notify.serializers import (CreateMailListSerializer,
                                             FetchMailListSerializer,
                                             )
from django.contrib.sites.shortcuts import get_current_site


# Helper response format method
def serialize_queryset(queryset):
    serialized_queryset = []
    for qs in queryset:
        data = {
            'id': qs.id,
            'description': qs.description,
            'verb': qs.verb,
            'unread': qs.unread,
            'emailed': qs.emailed,
            'recipient': qs.recipient.username,
            'actor': qs.actor.username,
            'timestamp': qs.timestamp,
            'data': qs.data,
        }
        serialized_queryset.append(data)
    return serialized_queryset
# Create your views here.


class FetchMailListView(ListAPIView):
    """
    Fetch all mail list objects from the mail list table
    """
    queryset = MailList.objects.all()
    serializer_class = FetchMailListSerializer
    permission_classes = (IsAuthenticated,)


class FetchUpdateMailList(GenericAPIView):
    """ Fetch or create a new mmail list object for the logged in user"""
    serializer_class = CreateMailListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """"""
        mail_list_obj = MailList.objects.get_or_create(user=request.user)[0]
        serialized_mail_list_obj = FetchMailListSerializer(mail_list_obj)

        return Response(serialized_mail_list_obj.data,
                        status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Update notification subscription status for a logged in user
        by changing the email or push notification status to false.
        opt-in and out of notifications

        """
        mail_list_obj = MailList.objects.get_or_create(user=request.user)[0]
        data = request.data
        serialized_data = self.serializer_class(
            instance=mail_list_obj, data=data, context=request, partial=True
        )
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(serialized_data.data, status=status.HTTP_200_OK)


class FetchAllNotifications(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_notifications = Notifier.fetch_all_notifications(
            user=request.user)

        if user_notifications.count() == 0:
            return Response(dict(
                message='You currently dont have any notifications')
            )

        data = serialize_queryset(user_notifications)
        return Response(
            {'count': user_notifications.count(),
             'notifications': data})


class FetchAllUnReadNotifications(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        unread_notifications = Notifier.fetch_unread_notifications(
            user=request.user)
        if unread_notifications.count() == 0:
            return Response(dict(
                message='You currently dont have any unread notifications')
            )

        return Response(
            {'count': unread_notifications.count(),
             'notifications': serialize_queryset(unread_notifications)})


class FetchAllReadNotifications(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        read_notifications = Notifier.fetch_read_notifications(
            user=request.user)
        if read_notifications.count() == 0:
            return Response(dict(
                message='You currently dont have any read notifications')
            )

        return Response(
            {'count': read_notifications.count(),
             'notifications': serialize_queryset(read_notifications)})


class MarkAllNotificationsAsRead(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_notifications = Notifier.fetch_unread_notifications(
            user=request.user)
        if user_notifications.count() == 0:
            return Response(dict(
                message='You currently dont have any notifications')
            )
        user_notifications.mark_all_as_read()

        return Response(
            dict(message='All notifications marked as read')
        )
