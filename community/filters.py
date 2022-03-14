from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from community.models import Community, Subscription
from community.serializers.community import CommunitySerializer
from globals import UserGlobalSerializer, CommunityGlobalSerializer


class TopCommunitiesList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        communities = []
        serializer = CommunitySerializer(communities, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribedCommunityFilter(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        search = request.GET.get("search")
        if search:
            subscriptions = Subscription.objects.filter(
                is_approved=True,
                is_banned=False,
                subscriber=request.user,
                community__name__contains=search,
            )
        else:
            subscriptions = Subscription.objects.filter(
                is_approved=True, is_banned=False, subscriber=request.user
            )
        communities = []
        [communities.append(subscription.community) for subscription in subscriptions]
        return Response(
            {
                "count": subscriptions.count(),
                "results": CommunityGlobalSerializer(communities, many=True).data,
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
            valid_subscriptions = Subscription.objects.filter(
                community=community, is_approved=True, is_banned=False
            )
        else:
            valid_subscriptions = Subscription.objects.filter(
                community=community,
                is_approved=True,
                is_banned=False,
                subscriber__username__contains=search,
            )
        users = []
        [users.append(subscription.subscriber) for subscription in valid_subscriptions]
        return Response(UserGlobalSerializer(users, many=True).data, status=status.HTTP_200_OK)
