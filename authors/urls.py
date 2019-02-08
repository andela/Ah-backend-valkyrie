from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg  import openapi
from django.conf import settings
from django.views.static import serve


schema_view = get_schema_view(
    openapi.Info(
        title="Authors Haven",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('authors.apps.authentication.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-json'),
    path('api/v1/', include((
        'authors.apps.authentication.social_auth.urls', 'authentication'
    ), namespace='authentication')),
    path('api/v1/articles/', include('authors.apps.articles.urls')),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('api/v1/', include('authors.apps.profiles.urls')),
    path('api/v1/articles/', include('authors.apps.comments.urls')),
    path('api/v1/', include('authors.apps.ratings.urls')),

    path('api/v1/', include('authors.apps.notify.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url('media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]