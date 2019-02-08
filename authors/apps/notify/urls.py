from django.urls import path

from authors.apps.notify.views import (
    FetchMailListView, FetchUpdateMailList,
    FetchAllNotifications, FetchAllUnReadNotifications,
    FetchAllReadNotifications, MarkAllNotificationsAsRead
)


urlpatterns = [
    path('mail_list', FetchMailListView.as_view(), name='mail-list'),
    path('mail_list_subscribe', FetchUpdateMailList.as_view(),
         name='mail-list-status'),
    path('notifications/', FetchAllNotifications.as_view(),
         name='all-notifications'),
    path('notifications/unread', FetchAllUnReadNotifications.as_view(),
         name='unread-notifications'),
    path('notifications/read', FetchAllReadNotifications.as_view(),
         name='read-notifications'),
    path('notifications/mark-as-read', MarkAllNotificationsAsRead.as_view(),
         name='mark-all-as-read'),
]
