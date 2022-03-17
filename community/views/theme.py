from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from community.permissions import IsCommunityModerator
from community.models import Community
from community.serializers.community import CommunitySerializer
from community.serializers.theme import ThemeSerializer
from community.sub_models.theme import Theme


class UpdateCommunityTheme(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def patch(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        serializer = ThemeSerializer(
            community.theme, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
