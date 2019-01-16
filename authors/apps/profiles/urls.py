from django.urls import path

from .views import ProfileRetrieveAPIView

urlpatterns = [
    path('profiles/<str:username>', ProfileRetrieveAPIView.as_view(), name='profile'),
]