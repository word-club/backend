from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from community.serializer import *


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    search_fields = ["name"]


class RemoveCommunityDisableNotification(APIView):
    @staticmethod
    def delete(request, pk):
        item = get_object_or_404(CommunityDisableNotifications, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityRule(APIView):
    @staticmethod
    def delete(request, pk):
        rule = get_object_or_404(CommunityRule, pk=pk)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityCover(APIView):
    @staticmethod
    def delete(request, pk):
        cover = get_object_or_404(CommunityCover, pk=pk)
        cover.image.delete()
        cover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityAvatar(APIView):
    @staticmethod
    def delete(request, pk):
        avatar = get_object_or_404(CommunityAvatar, pk=pk)
        avatar.image.delete()
        avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityReport(APIView):
    @staticmethod
    def delete(request, pk):
        report = get_object_or_404(CommunityReport, pk=pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnSubscribeCommunity(APIView):
    @staticmethod
    def delete(request, pk):
        report = get_object_or_404(CommunitySubscription, pk=pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportACommunity(APIView):
    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {"community": community, "request": request}
        serializer = ReportCommunitySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeToACommunity(APIView):
    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {"community": community, "request": request}
        serializer = SubscribeCommunitySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DisableNotificationsForACommunity(APIView):
    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {"community": community, "request": request}
        serializer = DisableNotificationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityAvatar(APIView):
    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {"community": community, "request": request}
        serializer = CommunityAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityCover(APIView):
    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {"community": community, "request": request}
        serializer = CommunityCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetActiveCommunityAvatar(APIView):
    @staticmethod
    def post(request, pk):
        community_avatar = get_object_or_404(CommunityAvatar, pk=pk)
        all_avatars = CommunityAvatar.objects.filter(
            community=community_avatar.community, is_active=True
        )
        for item in all_avatars:
            item.is_active = False
            item.save()
        community_avatar.is_active = True
        community_avatar.save()
        return Response(status=status.HTTP_200_OK)


class SetActiveCommunityCover(APIView):
    @staticmethod
    def post(request, pk):
        community_cover = get_object_or_404(CommunityAvatar, pk=pk)
        all_covers = CommunityCover.objects.filter(
            community=community_cover.community, is_active=True
        )
        for item in all_covers:
            item.is_active = False
            item.save()
        community_cover.is_active = True
        community_cover.save()
        return Response(status=status.HTTP_200_OK)
