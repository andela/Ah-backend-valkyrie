from rest_framework import serializers
from authors.apps.comments.models import Comment
from ..authentication.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ["author", "article"]
        fields = ("id", "body", "createdAt", "updatedAt", "author")