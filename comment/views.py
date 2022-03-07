from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import helper
from account.permissions import IsOwner
from comment.helper import check_comment_update_date_limit
from comment.serializers import *
from publication.models import Publication
from publication.permissions import IsPublicationAuthor, IsPublished


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

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = CommentSerializer(comment, context={"user": self.request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPublicationComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPublished]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {"publication": publication, "request": request}
        serializer = CommentPostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsPublicationAuthor]

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        check_comment_update_date_limit(comment)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
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


class CommentPinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPublicationAuthor]

    def patch(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        if comment.is_pinned:
            return Response(status=status.HTTP_200_OK)
        comment.is_pinned = True
        comment.pinned_at = timezone.now()
        comment.pinned_by = request.user
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
