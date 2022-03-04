from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from community.models import Community, CommunitySubscription
from community.serializer import CommunitySerializer
from globals import UserGlobalSerializer


class SubscribedCommunityFilter(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        search = request.GET.get("search")
        if search:
            items = CommunitySubscription.objects.filter(
                is_approved=True,
                is_banned=False,
                subscriber=request.user,
                community__name__contains=search,
            )
        else:
            items = CommunitySubscription.objects.filter(
                is_approved=True, is_banned=False, subscriber=request.user
            )
        communities = []
        [communities.append(subscription.community) for subscription in items]
        return Response(
            {
                "count": items.count(),
                "results": CommunitySerializer(communities, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class CommunitySubscribersFilter(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        community = get_object_or_404(Community, pk=pk)
        search = request.GET.get("search")
        if not search:
            valid_subscriptions = CommunitySubscription.objects.filter(
                community=community, is_approved=True, is_banned=False
            )
        else:
            valid_subscriptions = CommunitySubscription.objects.filter(
                community=community,
                is_approved=True,
                is_banned=False,
                subscriber__username__contains=search,
            )
        users = []
        [users.append(subscription.subscriber) for subscription in valid_subscriptions]
        return Response(
            UserGlobalSerializer(users, many=True).data, status=status.HTTP_200_OK
        )
