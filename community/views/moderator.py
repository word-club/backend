from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404

from community.serializers.moderator import ModeratorSerializer
from community.sub_models.moderator import Moderator
from community.models import Community
from community.permissions import IsCommunityModerator


class AddModerator(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request, "role": "mod"}
        serializer = ModeratorSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSubModerator(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request, "role": "sub"}
        serializer = ModeratorSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeratorDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def get(self, request, pk):
        moderator = get_object_or_404(Moderator, pk=pk)
        self.check_object_permissions(request, moderator)
        serializer = ModeratorSerializer(moderator)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        moderator = get_object_or_404(Moderator, pk=pk)
        self.check_object_permissions(request, moderator)
        moderator.delete()
        return Response(status=status.HTTP_200_OK)
