from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Profile
from account.permissions import IsOwner
from avatar.models import Avatar
from avatar.serializers import (AvatarSerializer, CommunityAvatarSerializer,
                                ProfileAvatarSerializer)
from community.models import Community
from community.permissions import IsCommunityModerator


class AddProfileAvatarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        self.check_object_permissions(request, profile)
        context = {"profile": profile, "request": request}
        serializer = ProfileAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityAvatarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner, IsAdminUser]

    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, avatar)
        serializer = AvatarSerializer(avatar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        toggle active status
        """
        cover = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, cover)
        cover.is_active = not cover.is_active
        cover.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, avatar)
        avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
