from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

import helper
from account.permissions import IsOwner
from community.models import (
    Community,
    CommunitySubscription,
    CommunityRule,
    CommunityAdmin,
    CommunityAuthorizationCode,
    CommunityTheme,
)
from community.permissions import (
    IsNotASubscriber,
    IsCommunityAdministrator,
    IsSubscriber,
)
from community.serializer import (
    CommunitySerializer,
    CommunityRetrieveSerializer,
    CommunityRuleSerializer,
    CommunitySubscriptionSerializer,
    CommunityAdminSerializer,
    CommunityThemeSerializer,
)


class CommunityViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    serializer_class = CommunitySerializer
    search_fields = ["name"]
    filterset_fields = [
        "type",
        "is_authorized",
        "contains_adult_content",
        "completed_registration_steps",
        "created_by",
    ]

    def get_queryset(self):
        filterset, sort_string = helper.get_viewset_filterset(
            self.request, self.filterset_fields, "date_of_registration"
        )
        return Community.objects.filter(
            ~Q(type__exact="private"),
            **filterset,
        ).order_by(sort_string)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        depth = 0
        try:
            depth = int(self.request.query_params.get("depth", 0))
        except ValueError:
            pass
        context["depth"] = depth
        return context


class CommunityDetail(APIView):
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


class SubscribeToACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsNotASubscriber]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        subscription = CommunitySubscription.objects.create(
            community=community, subscriber=request.user
        )
        if community.type == "public":
            subscription.is_approved = True
            subscription.approved_at = timezone.now()
            subscription.save()
        serializer = CommunitySubscriptionSerializer(subscription, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class AddCommunityHashtag(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        # TODO: link hashtag with the community
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


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
    permission_classes = [IsAuthenticated, IsCommunityAdministrator]

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        # TODO: unlink hashtag from the community
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


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


class TopCommunitiesList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        communities = []
        serializer = CommunitySerializer(communities, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewACommunity(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request, pk=None):
        community = get_object_or_404(Community, pk=pk)
        community.views += 1
        community.save()
        serializer = CommunityRetrieveSerializer(community, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
