from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import ProfileAvatar, ProfileCover, Profile
from account.permissions import IsOwner
from account.serializers.user import ProfileAvatarSerializer, ProfileCoverSerializer


class ProfileAvatarViewSet(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ProfileAvatar.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = ProfileAvatarSerializer
    filterset_fields = ["is_active", "profile"]

    def destroy(self, request, *args, **kwargs):
        profile_avatar = self.get_object()
        profile_avatar.image.delete()
        profile_avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileCoverViewSet(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ProfileCover.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = ProfileCoverSerializer
    filterset_fields = ["is_active", "profile"]

    def destroy(self, request, *args, **kwargs):
        profile_cover = self.get_object()
        profile_cover.image.delete()
        profile_cover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddProfileAvatarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        self.check_object_permissions(request, profile)
        context = {"profile": profile}
        serializer = ProfileAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProfileCoverView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        self.check_object_permissions(request, profile)
        context = {"profile": profile}
        serializer = ProfileCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
