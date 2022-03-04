from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from account.models import Profile
from account.permissions import IsOwner
from cover.models import Cover
from community.models import Community
from community.permissions import IsCommunityAdministrator
from cover.serializers import (
    ProfileCoverSerializer,
    CommunityCoverSerializer,
    CoverSerializer,
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
    permission_classes = [IsCommunityAdministrator]

    def post(self, request):
        community = get_object_or_404(Community, user=request.user)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoverDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner, IsAdminUser]

    def get(self, request, pk):
        cover = get_object_or_404(Cover, pk=pk)
        self.check_object_permissions(request, cover)
        serializer = CoverSerializer(cover)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cover = get_object_or_404(Cover, pk=pk)
        self.check_object_permissions(request, cover)
        cover.image.delete()
        cover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
