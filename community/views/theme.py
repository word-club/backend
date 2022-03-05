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


class AddCommunityTheme(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = ThemeSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCommunityTheme(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def patch(self, request, pk):
        community_theme = get_object_or_404(Theme, pk=pk)
        self.check_object_permissions(request, community_theme)
        serializer = ThemeSerializer(
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
        community_theme = get_object_or_404(Theme, pk=pk)
        self.check_object_permissions(request, community_theme)
        community_theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
