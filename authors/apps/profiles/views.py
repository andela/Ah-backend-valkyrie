from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer
from .exceptions import ProfileDoesNotExist


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
