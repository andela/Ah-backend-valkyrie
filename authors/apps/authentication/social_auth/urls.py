from django.urls import path
from .api_views import (
    FacebookSociaLoginView, GoogleSociaLoginView, TwitterSociaLoginView
)

urlpatterns = [
    path('auth/facebook/', FacebookSociaLoginView.as_view()),
    path('auth/google/', GoogleSociaLoginView.as_view()),
    path('auth/twitter/', TwitterSociaLoginView.as_view()),
]
