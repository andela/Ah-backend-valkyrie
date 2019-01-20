from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models
from . import serializers


class ListCreateArticle(generics.ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ListCreateTag(generics.ListCreateAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class RetrieveUpdateDestroyTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class LikeArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikeArticleSerializer

    def post(self, request):
        data = {
            "article_id": request.data.get('article'),
            "user_id": request.user.id,
            "like": request.data.get('like')
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
