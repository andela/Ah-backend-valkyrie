from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer
from .exceptions import ProfileDoesNotExist


class ProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)
    permission_classes = (AllowAny,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist
        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)
