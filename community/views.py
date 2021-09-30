from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from community.permissions import (
    IsCommunityAdministrator,
    IsSubscriber,
    IsNotASubscriber,
)
from community.serializer import *


class CommunityViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in ["delete", "update", "partial_update"]:
            return [IsCommunityAdministrator]
        elif self.action in ["list", "retrieve"]:
            return [IsAdminUser]
        elif self.action == "create":
            return []  # TODO: maybe an authorized user


class RemoveCommunityDisableNotification(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        item = get_object_or_404(CommunityDisableNotifications, pk=pk)
        self.check_object_permissions(request, item)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityRule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def delete(self, request, pk):
        rule = get_object_or_404(CommunityRule, pk=pk)
        self.check_object_permissions(request, rule)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityCover(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def delete(self, request, pk):
        cover = get_object_or_404(CommunityCover, pk=pk)
        self.check_object_permissions(request, cover)
        cover.image.delete()
        cover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityAvatar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def delete(self, request, pk):
        avatar = get_object_or_404(CommunityAvatar, pk=pk)
        self.check_object_permissions(request, avatar)
        avatar.image.delete()
        avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteCommunityReport(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def delete(self, request, pk):
        report = get_object_or_404(CommunityReport, pk=pk)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnSubscribeCommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSubscriber]

    def delete(self, request, pk):
        subscription = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, subscription.community)

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSubscriber]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = ReportCommunitySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeToACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsNotASubscriber]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = SubscribeCommunitySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DisableNotificationsForACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSubscriber]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = DisableNotificationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityAvatar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityCover(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityCoverSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetActiveCommunityAvatar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community_avatar = get_object_or_404(CommunityAvatar, pk=pk)
        self.check_object_permissions(request, community_avatar)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community_cover = get_object_or_404(CommunityAvatar, pk=pk)
        self.check_object_permissions(request, community_cover)
        all_covers = CommunityCover.objects.filter(
            community=community_cover.community, is_active=True
        )
        for item in all_covers:
            item.is_active = False
            item.save()
        community_cover.is_active = True
        community_cover.save()
        return Response(status=status.HTTP_200_OK)


class AddCommunityHashtag(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityHashtagSerializer(request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCommunityHashtag(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def delete(self, request, pk):
        community_hashtag = get_object_or_404(CommunityHashtag, pk=pk)
        self.check_object_permissions(request, community_hashtag)
        community_hashtag.delete()
        return Response(status=status.HTTP_200_OK)


class AddCommunityAdmin(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityAdminSerializer(request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCommunityAdmin(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def delete(self, request, pk):
        community_admin = get_object_or_404(CommunityAdmin, pk=pk)
        self.check_object_permissions(request, community_admin)
        community_admin.delete()
        return Response(status=status.HTTP_200_OK)


class RequestCommunityAuthorization(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        if community.email:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"details": "Community does not have email set."}
            )
        if community.is_authorized:
            return Response(status=status.HTTP_204_NO_CONTENT, data={"details": "Community is already authorized."})
        codes = CommunityAuthorizationCode.objects.filter(community=community)
        [code.delete() for code in codes]  # delete every pre-existing codes
        code = CommunityAuthorizationCode.objects.create(community=community)
        mail_subject = "Authorize Community"
        message = render_to_string(
            "authorize_community.html",
            {
                "request": request,
                "user": request.user,
                "domain": get_current_site(request).domain,
                "code": code.code,
            },
        )
        send_mail(
            mail_subject,
            message="AuthorizeCommunity",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[community.email],
            html_message=message,
        )
        return Response(status=status.HTTP_200_OK)


class ConfirmCommunityAuthorization(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community_authorize_code = get_object_or_404(CommunityAuthorizationCode, pk=pk)
        self.check_object_permissions(request, community_authorize_code)
        community_to_authorize = community_authorize_code.community
        community_to_authorize.is_authorized = True
        community_to_authorize.authorized_at = timezone.now()
        community_to_authorize.save()
        community_authorize_code.delete()
        return Response(status=status.HTTP_200_OK)
