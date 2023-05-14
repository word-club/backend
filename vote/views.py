from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner, IsSuperUser
from comment.models import Comment
from publication.models import Publication
from vote.models import Vote
from vote.serializers import VoteDetailSerializer


class AddPublicationUpVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        upvote, created = Vote.objects.get_or_create(
            publication=publication, up=True, created_by=request.user
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddCommentUpVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        upvote, created = Vote.objects.get_or_create(
            comment=comment, up=True, created_by=request.user
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddPublicationDownVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        upvote, created = Vote.objects.get_or_create(
            publication=publication, up=False, created_by=request.user
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddCommentDownVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        upvote, created = Vote.objects.get_or_create(
            comment=comment, up=False, created_by=request.user
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class VoteDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def get(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk)
        self.check_object_permissions(request, vote)
        serializer = VoteDetailSerializer(vote)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk)
        self.check_object_permissions(request, vote)
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VoteList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        self.check_object_permissions(request, request.user)
        votes = Vote.objects.all()
        serializer = VoteDetailSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
