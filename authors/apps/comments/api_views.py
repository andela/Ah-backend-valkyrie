from rest_framework import generics
from rest_framework import permissions
from authors.apps.articles.models import Article
from rest_framework import response
from .models import Comment, CommentReaction
from rest_framework import status
from .serializers import CommentSerializer, CommentReactionSerializer
from .renderers import CommentsRenderer
from authors.apps.authentication.models import User
from django.db.models import Q
from authors.apps.core import authority
from rest_framework.exceptions import NotAcceptable
from django.shortcuts import get_object_or_404, get_list_or_404


class CommentList(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    renderer_classes = (CommentsRenderer,)
    lookup_field = "slug"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        comment = request.data.get("comment", {})
        serializer = CommentList.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        user = request.user
        slug = kwargs["slug"]
        articles = Article.objects.filter(slug=slug).first()
        current_user = User.objects.filter(email=user).first()
        article_id = Article.objects.filter(slug=slug).first().id
        author_id = User.objects.filter(email=user).first().id
        group = Comment.objects.filter(
            Q(
                body=comment['body']
            ) & Q(
                article_id=article_id
                ) & Q(
                    author_id=author_id
                    )
        )
        if group.exists():
            return response.Response(
                                {"message": "You can't give the same comment twice on the same article"}, status=status.HTTP_409_CONFLICT,)  
        serializer.save(author=current_user, article=articles)
        return response.Response(
            {"message": "comment created ", "comment": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        """ Return a view using the slug """
        slug = self.kwargs["slug"]
        _id = Article.objects.filter(slug=slug).first().id
        comments = Comment.objects.filter(article_id=_id).all()
        return comments


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        authority.IsOwnerOrReadOnly,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_fields = ["pk", "slug"]


class CommentLike(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer

    def post(self, request, *args, **kwargs):
        '''enables one to post a like  to a comment'''
        user = request.user
        current_user = User.objects.filter(email=user).first()
        user_id = current_user.id
        _id = kwargs['pk']
        
        liked_group = CommentReaction.objects.filter(
            Q(like=True) & Q(user_id=user_id) & Q(comment_id=_id))

        disliked_group = CommentReaction.objects.filter(
            Q(like=False) & Q(user_id=user_id) & Q(comment_id=_id))

        if liked_group.exists():
            CommentReaction.objects.filter(
                Q(user_id=user_id) & Q(comment_id=_id)).update(like=False)
            return response.Response(
                {"message": "comment disliked"}, status=status.HTTP_200_OK)

        elif disliked_group.exists():
            CommentReaction.objects.filter(
                Q(user_id=user_id) & Q(comment_id=_id)).update(like=True)
            return response.Response(
                {"message": "comment liked"}, status=status.HTTP_200_OK)

        like_data = request.data.get("like", {})
        serializer = self.serializer_class(data=like_data)
        serializer.is_valid(raise_exception=True)
        comment = get_object_or_404(Comment, pk=_id)
        serializer.save(comment=comment, user=current_user)
        return response.Response({'message': 'Comment liked',
                                  'comment_like': serializer.data},
                                 status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        '''Enables one to get likes and dislikes '''
        _id = kwargs['pk']
        _bool = True
        state = get_list_or_404(
            CommentReaction, comment_id=_id 
        )
        likes = [item for item in state if item.like == _bool]
        serializer = self.serializer_class(state, many=True)
        return response.Response({"reactions": serializer.data,
                                  "likes_count": len(likes)})


class CommentDislike(generics.DestroyAPIView):
    '''Enables one to dislike a comment '''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer
    lookup_fields = ["pk"]
