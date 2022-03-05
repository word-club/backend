from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from community.models import Community
from community.permissions import IsCommunityModerator


class AddCommunityHashtag(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        # TODO: link hashtag with the community
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class RemoveCommunityHashtag(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        # TODO: unlink hashtag from the community
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
