from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('authors.apps.authentication.urls')),

    path('api/v1/', include((
        'authors.apps.authentication.social_auth.urls', 'authentication'
    ), namespace='authentication')),
    path('api/v1/articles/', include('authors.apps.articles.urls')),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('api/v1/', include('authors.apps.profiles.urls')),
    path('api/v1/articles/', include('authors.apps.comments.urls')),
    path('api/v1/', include('authors.apps.ratings.urls')),
]
