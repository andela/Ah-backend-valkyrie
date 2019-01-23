from rest_framework import serializers
from authors.apps.comments.models import Comment, CommentReaction
from ..authentication.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ["author", "article"]
        fields = ("id", "body", "createdAt", "updatedAt", "author")
        

class CommentReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = CommentReaction
        fields = ("id", "comment", "like", "user")
        read_only_fields = ['comment', 'user']

