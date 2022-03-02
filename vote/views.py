from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

from account.permissions import IsOwner
from comment.models import Comment
from publication.models import Publication
from vote.models import Vote


class AddPublicationUpVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        upvote, created = Vote.objects.get_or_create(
            Vote, publication=publication, up=True
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddCommentUpVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        upvote, created = Vote.objects.get_or_create(Vote, comment=comment, up=True)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddPublicationDownVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        upvote, created = Vote.objects.get_or_create(
            Vote, publication=publication, up=False
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddCommentDownVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        upvote, created = Vote.objects.get_or_create(Vote, comment=comment, up=False)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class DestroyVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk)
        self.check_object_permissions(request, vote)
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
