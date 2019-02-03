from rest_framework import serializers
from authors.apps.comments.models import Comment, CommentHistory, CommentReaction
from authors.apps.authentication.serializers import UserSerializer


class CommentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentHistory
        fields = ["id", "body", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comment_history = CommentHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'body',
            'updatedAt',
            'createdAt',
            'author',
            'comment_history'
        ]
        read_only_fields = ["author", "article"]


class CommentReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = CommentReaction
        fields = ("id", "comment", "like", "user")
        read_only_fields = ['comment', 'user']
