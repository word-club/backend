from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Profile
from account.permissions import IsOwner
from community.models import Community
from community.permissions import IsCommunityModerator
from cover.models import Cover
from cover.serializers import (
    CommunityCoverSerializer,
    CoverSerializer,
    ProfileCoverSerializer,
)


class AddProfileCoverView(APIView):
    permission_classes = [IsOwner]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        self.check_object_permissions(request, profile)
        context = {"profile": profile, "request": request}
        serializer = ProfileCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityCoverView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoverDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def get(self, request, pk):
        cover = get_object_or_404(Cover, pk=pk)
        self.check_object_permissions(request, cover)
        serializer = CoverSerializer(cover)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cover = get_object_or_404(Cover, pk=pk)
        self.check_object_permissions(request, cover)
        cover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleActiveStatus(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        """
        toggle active status
        """
        cover = get_object_or_404(Cover, pk=pk)
        self.check_object_permissions(request, cover)

        Cover.objects.filter(is_active=True, community=cover.community, profile=cover.profile).update(is_active=False)

        cover.is_active = True
        cover.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        cover = get_object_or_404(Cover, pk=pk)
        self.check_object_permissions(request, cover)
        if not cover.is_active:
            return Response(status=status.HTTP_204_NO_CONTENT)
        cover.is_active = False
        cover.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
