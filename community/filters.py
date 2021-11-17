from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from community.models import CommunitySubscription
from community.serializer import SubscribeCommunitySerializer


class SubscribedCommunityFilter(APIView):
    @staticmethod
    def get(request):
        search = request.get("search")
        if search:
            items = CommunitySubscription.objects.filter(
                is_approved=True,
                is_banned=False,
                subscriber=request.user,
                community__name__contains=search
            )
        else: items = CommunitySubscription.objects.filter(is_approved=True, is_banned=False, subscriber=request.user)
        return Response(SubscribeCommunitySerializer(items).data, status=status.HTTP_200_OK)

