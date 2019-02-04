from django.urls import path

from .views import RatingAPIView


urlpatterns = [
    path('articles/<slug>/rating', RatingAPIView.as_view(), name='rating')
]
