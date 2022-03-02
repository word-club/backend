from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import helper
from account.permissions import IsOwner
from comment.serializers import *
from publication.permissions import IsPublicationAuthor


def check_comment_update_date_limit(obj):
    """
    :param obj: Comment instance
    :return: void if comment date limit is not reached
        Response(403) if publication update date limit reached
    """
    now = timezone.now()
    if not obj.published_at:
        return
    diff = now - obj.created_at
    limit = Administration.objects.first()
    if diff.days > limit.comment_update_limit:
        return Response(
            {
                "detail": "Sorry, you cannot update the comment after {} days.".format(
                    limit.comment_update_limit
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    filterset_fields = ["publication", "reply", "is_pinned", "created_by"]
    serializer_class = CommentSerializer

    def get_queryset(self):
        filterset, sort_string = helper.get_viewset_filterset(
            self.request, self.filterset_fields, "created_at"
        )
        return Comment.objects.filter(**filterset).order_by(sort_string)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def retrieve(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, context={"user": self.request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPublicationComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        context = {"publication": publication, "request": request}
        serializer = CommentPostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDestroyCommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsPublicationAuthor]

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        check_comment_update_date_limit(comment)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(
            comment, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment_images = CommentImage.objects.filter(comment=comment)
        [img.image.delete() for img in comment_images]
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveCommentImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        comment_image = get_object_or_404(CommentImage, pk=pk)
        self.check_object_permissions(request, comment_image.comment)
        comment_image.image.delete()
        comment_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveCommentImageUrlView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        comment_image_url = get_object_or_404(CommentImageUrl, pk=pk)
        self.check_object_permissions(request, comment_image_url.comment)
        comment_image_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyCommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        context = {"comment": comment, "user": request.user}
        serializer = ReplyPostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HideCommentForMe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        instance = get_object_or_404(Comment, pk=pk)
        hidden_status, created = HideComment.objects.get_or_create(
            comment=instance, created_by=request.user
        )
        if created:
            return Response(
                HideCommentSerializer(hidden_status).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveHiddenStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        instance = get_object_or_404(HideComment, pk=pk)
        self.check_object_permissions(request, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentPinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPublicationAuthor]

    def patch(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        if comment.is_pinned:
            return Response(status=status.HTTP_200_OK)
        comment.is_pinned = True
        comment.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        if comment.is_pinned:
            comment.is_pinned = False
            comment.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)
