from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404

from community.sub_models.rule import Rule
from community.models import Community
from community.permissions import IsCommunityModerator


class PatchDeleteCommunityRule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def patch(self, request, pk):
        rule = get_object_or_404(Rule, pk=pk)
        self.check_object_permissions(request, rule)
        serializer = RuleSerializer(
            instance=rule, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rule = get_object_or_404(Rule, pk=pk)
        self.check_object_permissions(request, rule)
        rule.delete()
        return Response(status=status.HTTP_200_OK)


class AddCommunityRule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = RuleSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
