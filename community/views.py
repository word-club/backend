from django.conf import settings
from django.db.utils import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import viewsets, status, mixins
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


class CommunityViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    search_fields = ["name"]
    filterset_fields = [
        "type",
        "is_authorized",
        "contains_adult_content",
        "completed_registration_steps",
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        depth = 0
        try:
            depth = int(self.request.query_params.get("depth", 0))
        except ValueError:
            pass
        context["depth"] = depth
        return context

    def get_permissions(self):
        if self.action in ["list"]:
            return [IsAdminUser()]
        else:
            return []


class PatchDeleteCommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def get(self, request, pk=None):
        community = get_object_or_404(Community, pk=pk)
        serializer = CommunityRetrieveSerializer(
            community, context={"depth": 2, "user": request.user}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        serializer = CommunitySerializer(
            data=request.data, instance=community, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        community.delete()
        return Response(status=status.HTTP_200_OK)


class RemoveCommunityDisableNotification(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        subscription = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, subscription)
        if not subscription.disable_notification:
            return Response(status=status.HTTP_200_OK)
        subscription.disable_notification = False
        subscription.save()
        return Response(status=status.HTTP_201_CREATED)


class PatchDeleteCommunityRule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def patch(self, request, pk):
        rule = get_object_or_404(CommunityRule, pk=pk)
        self.check_object_permissions(request, rule)
        serializer = CommunityRuleSerializer(
            instance=rule, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rule = get_object_or_404(CommunityRule, pk=pk)
        self.check_object_permissions(request, rule)
        rule.delete()
        return Response(
            CommunitySerializer(rule.community).data, status=status.HTTP_200_OK
        )


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

        subscription = get_object_or_404(
            CommunitySubscription, community=pk, subscriber=request.user
        )
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DisableNotificationsForACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSubscriber]

    def post(self, request, pk):
        subscription = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, subscription.community)

        if subscription.disable_notification:
            return Response(status=status.HTTP_200_OK)
        subscription.disable_notification = True
        subscription.save()
        return Response(status=status.HTTP_201_CREATED)


class AddCommunityAvatar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityAvatarSerializer(data=request.data, context=context)
        if serializer.is_valid():
            previous_avatar = CommunityAvatar.objects.filter(community=community)
            [img.image.delete() for img in previous_avatar]
            [img.delete() for img in previous_avatar]
            serializer.save()
            return Response(
                CommunitySerializer(community).data, status=status.HTTP_201_CREATED
            )
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
            previous_cover = CommunityCover.objects.filter(community=community)
            [img.image.delete() for img in previous_cover]
            [img.delete() for img in previous_cover]
            serializer.save()
            return Response(
                CommunitySerializer(community).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityHashtag(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        serializer = CommunityHashtagPostSerializer(data=request.data)
        if serializer.is_valid():
            errors = {}
            validated_data = serializer.validated_data
            tags = validated_data.get("tags")
            for tag in tags:
                try:
                    CommunityHashtag.objects.create(tag=tag, community=community)
                except IntegrityError:
                    errors[tag.id] = "cannot add non-unique tag {}".format(tag.tag)
            return Response(
                CommunitySerializer(community, context={"depth": 3}).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityRule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityRuleSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(
                CommunitySerializer(community).data, status=status.HTTP_201_CREATED
            )
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
        serializer = CommunityAdminSerializer(data=request.data, context=context)
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
        if not community.email:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Community does not have email set."},
            )
        if community.is_authorized:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={"detail": "Community is already authorized."},
            )
        codes = CommunityAuthorizationCode.objects.filter(
            community=community, created_by=request.user
        )
        [code.delete() for code in codes]  # delete every pre-requested codes
        code = CommunityAuthorizationCode.objects.create(
            community=community, created_by=request.user
        )
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

    def post(self, request, code):
        community_authorize_code = get_object_or_404(
            CommunityAuthorizationCode, code=code
        )
        self.check_object_permissions(request, community_authorize_code)
        community_to_authorize = community_authorize_code.community
        community_to_authorize.is_authorized = True
        community_to_authorize.authorized_at = timezone.now()
        community_to_authorize.save()
        community_authorize_code.delete()
        return Response(
            CommunitySerializer(community_to_authorize).data, status=status.HTTP_200_OK
        )


class AddCommunityTheme(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = CommunityThemeSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCommunityTheme(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def patch(self, request, pk):
        community_theme = get_object_or_404(CommunityTheme, pk=pk)
        self.check_object_permissions(request, community_theme)
        serializer = CommunityThemeSerializer(
            community_theme, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                CommunitySerializer(community_theme.community).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        community_theme = get_object_or_404(CommunityTheme, pk=pk)
        self.check_object_permissions(request, community_theme)
        community_theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcceptRejectACommunitySubscriber(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community_subscriber = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, community_subscriber)
        if community_subscriber.is_banned:
            return Response(
                {"detail": "Cannot accept a banned subscriber."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            if community_subscriber.is_accepted:
                return Response({"detail": "Subscriber already accepted."})
            else:
                community_subscriber.is_accepted = True
                community_subscriber.accepted_at = timezone.now()
                community_subscriber.save()
                return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        community_subscriber = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, community_subscriber)
        community_subscriber.delete()
        return Response(status=status.HTTP_200_OK)


class BanUnBanACommunitySubscriber(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community_subscriber = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, community_subscriber)
        if community_subscriber.is_banned:
            return Response(
                {"detail": "Cannot ban an already banned subscriber."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            community_subscriber.is_banned = True
            community_subscriber.banned_at = timezone.now()
            community_subscriber.save()
            return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        community_subscriber = get_object_or_404(CommunitySubscription, pk=pk)
        self.check_object_permissions(request, community_subscriber)
        community_subscriber.is_banned = False
        community_subscriber.banned_at = None
        community_subscriber.save()
        return Response(status=status.HTTP_200_OK)


class SetProgressStepAsComplete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        progress_state = get_object_or_404(CommunityCreateProgress, pk=pk)
        self.check_object_permissions(request, progress_state)
        if progress_state.is_completed:
            return Response(status=status.HTTP_204_NO_CONTENT)
        progress_state.is_completed = True
        progress_state.save()
        community_serializer = CommunitySerializer(progress_state.community)
        return Response(community_serializer.data, status=status.HTTP_200_OK)


class SetProgressStepAsSkipped(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        progress_state = get_object_or_404(CommunityCreateProgress, pk=pk)
        self.check_object_permissions(request, progress_state)
        if progress_state.is_completed:
            return Response(
                {"detail": "Failed to skip. State is already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if progress_state.is_skipped:
            return Response(status=status.HTTP_204_NO_CONTENT)
        progress_state.is_skipped = True
        progress_state.save()
        community_serializer = CommunitySerializer(progress_state.community)
        return Response(community_serializer.data, status=status.HTTP_200_OK)


class CompleteRegistrationSteps(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        if community.completed_registration_steps:
            return Response(status=status.HTTP_200_OK)
        community.completed_registration_steps = True
        community.save()
        return Response(CommunitySerializer(community).data, status=status.HTTP_200_OK)


class BlockACommunity(APIView):
    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {"community": community, "request": request}
        serializer = CommunityBlockSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnBlockACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        block = get_object_or_404(BlockCommunity, pk=pk)
        self.check_object_permissions(request, block)
        block.delete()
        return Response(status=status.HTTP_200_OK)


class TopCommunitiesList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        communities = []
        serializer = CommunitySerializer(communities, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
