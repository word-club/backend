from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from account.permissions import IsOwner
from community.models import Community
from community.permissions import IsSubscriber, IsNotASubscriber, IsCommunityModerator
from community.serializers.subscription import SubscriptionSerializer
from community.sub_models.subscription import Subscription


class RemoveDisableNotification(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        self.check_object_permissions(request, subscription)
        if not subscription.disable_notification:
            return Response(status=status.HTTP_200_OK)
        subscription.disable_notification = False
        subscription.save()
        return Response(status=status.HTTP_201_CREATED)


class SubscriptionDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSubscriber]

    def delete(self, request, pk):
        subscription = get_object_or_404(Subscription, community=pk, subscriber=request.user)
        self.check_object_permissions(request, subscription.community)

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeToACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsNotASubscriber]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        subscription = Subscription.objects.create(community=community, subscriber=request.user)
        if community.type == "public":
            subscription.is_approved = True
            subscription.approved_at = timezone.now()
            subscription.save()
        serializer = SubscriptionSerializer(subscription, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DisableNotifications(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSubscriber]

    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        self.check_object_permissions(request, subscription.community)

        if subscription.disable_notification:
            return Response(status=status.HTTP_200_OK)
        subscription.disable_notification = True
        subscription.save()
        return Response(status=status.HTTP_201_CREATED)


class AcceptRejectASubscriber(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        self.check_object_permissions(request, subscription)
        if subscription.is_banned:
            return Response(
                {"detail": "Cannot accept a banned subscriber."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            if subscription.is_approved:
                return Response({"detail": "Subscriber already accepted."})
            else:
                subscription.is_approved = True
                subscription.accepted_at = timezone.now()
                subscription.save()
                return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        self.check_object_permissions(request, subscription)
        subscription.delete()
        return Response(status=status.HTTP_200_OK)


class BanUnBanASubscriber(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        self.check_object_permissions(request, subscription)
        if subscription.is_banned:
            return Response(
                {"detail": "Cannot ban an already banned subscriber."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            subscription.is_banned = True
            subscription.banned_at = timezone.now()
            subscription.save()
            return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        self.check_object_permissions(request, subscription)
        subscription.is_banned = False
        subscription.banned_at = None
        subscription.save()
        return Response(status=status.HTTP_200_OK)
