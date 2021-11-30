from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Profile
from account.serializers.user import UserRetrieveSerializer
from administration.models import Administration
from community.models import Community
from community.serializer import CommunityRetrieveSerializer

# TODO: replace with next line
administration = Administration.objects.first()
count = administration.top_count
# limit = administration.popularity_threshold
limit = 0


class TopView(APIView):
    @staticmethod
    def get(request):
        communities = Community.objects.filter(
            type__in=["public", "restricted"],
            popularity__gte=limit,
        ).order_by("-popularity")[:count]

        profiles = Profile.objects.filter(popularity__gte=limit).order_by(
            "-popularity"
        )[:count]
        users = []
        [users.append(profile.user) for profile in profiles]

        profiles = Profile.objects.filter(discussions__gte=limit,).order_by(
            "-discussions"
        )[:count]
        commentators = []
        [commentators.append(profile.user) for profile in profiles]

        context = {"user": request.user}

        return Response(
            {
                "communities": CommunityRetrieveSerializer(
                    communities, many=True, context=context
                ).data,
                "users": UserRetrieveSerializer(users, many=True, context=context).data,
                "commentators": UserRetrieveSerializer(
                    commentators, many=True, context=context
                ).data,
            },
            status=status.HTTP_200_OK,
        )
