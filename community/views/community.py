from django.db.models import Q

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

import helper
from community.models import Community
from community.permissions import (
    IsCommunityModerator,
)
from community.serializers.community import (
    CommunitySerializer,
    RetrieveSerializer,
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
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    def get(self, request, pk=None):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        serializer = RetrieveSerializer(
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


class ViewACommunity(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request, pk=None):
        community = get_object_or_404(Community, pk=pk)
        community.views += 1
        community.save()
        serializer = RetrieveSerializer(community, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

