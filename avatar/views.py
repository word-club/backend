from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Profile
from avatar.models import Avatar
from avatar.permissions import IsAvatarManager
from avatar.serializers import (
    AvatarSerializer,
    CommunityAvatarSerializer,
    ProfileAvatarSerializer,
)
from community.models import Community
from community.permissions import IsCommunityModerator


def set_active_status_for(avatar):
    """
    Set the active status for the avatar.
    """
    # set every avatar's active status to false first
    Avatar.objects.filter(
        is_active=True, community=avatar.community, profile=avatar.profile
    ).update(is_active=False)

    # toggle active status
    avatar.is_active = True
    avatar.save()


class AddProfileAvatarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = get_object_or_404(Profile, created_by=request.user)
        self.check_object_permissions(request, profile)
        context = {"profile": profile, "request": request}
        serializer = ProfileAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            av = serializer.save()
            # if request queryset has active param, then set avatar as active
            status_to_set = request.query_params.get("active", False)
            if status_to_set and status_to_set.lower() == "true":
                set_active_status_for(av)
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
            av = serializer.save()
            # if request queryset has active param, then set avatar as active
            status_to_set = request.query_params.get("active", False)
            if status_to_set and status_to_set.lower() == "true":
                set_active_status_for(av)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAvatarManager]

    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, avatar)
        serializer = AvatarSerializer(avatar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, avatar)
        avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleActiveStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAvatarManager]

    def post(self, request, pk):
        """
        set active status
        """
        avatar = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, avatar)

        if avatar.is_active:
            return Response(status=status.HTTP_204_NO_CONTENT)

        set_active_status_for(avatar)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        self.check_object_permissions(request, avatar)
        if not avatar.is_active:
            return Response(status=status.HTTP_204_NO_CONTENT)
        avatar.is_active = False
        avatar.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
