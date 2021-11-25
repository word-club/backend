from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Profile
from account.serializers.user import (
    ProfileAvatarSerializer,
    ProfileCoverSerializer,
    UserInfoSerializer,
)


class AddProfileAvatarView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request):
        profile = get_object_or_404(Profile, user=request.user)
        context = {"profile": profile}
        serializer = ProfileAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserInfoSerializer(profile.user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProfileCoverView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request):
        profile = get_object_or_404(Profile, user=request.user)
        context = {"profile": profile}
        serializer = ProfileCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserInfoSerializer(profile.user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
