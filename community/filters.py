from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from community.models import CommunitySubscription
from community.serializer import SubscribeCommunitySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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
        return Response(
            {
                "count": items.count(),
                "results": SubscribeCommunitySerializer(items, many=True).data
            }, status=status.HTTP_200_OK
        )
