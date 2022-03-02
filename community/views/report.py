from rest_framework.views import APIView

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from account.permissions import IsOwner
from community.permissions import (
    IsCommunityAdministrator,
    IsSubscriber,
)
from community.serializer import *


class ReportACommunity(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSubscriber]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        context = {"community": community, "request": request}
        serializer = ReportCommunitySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityReportDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner, IsCommunityAdministrator]

    def get(self, request, pk):
        report = get_object_or_404(CommunityReport, pk=pk)
        self.check_object_permissions(request, report)
        serializer = ReportCommunitySerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        report = get_object_or_404(CommunityReport, pk=pk)
        self.check_object_permissions(request, report)
        serializer = ReportCommunitySerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        report = get_object_or_404(CommunityReport, pk=pk)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResolveReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityAdministrator]

    def post(self, request, pk):
        report = get_object_or_404(CommunityReport, pk=pk)
        self.check_object_permissions(request, report)

        serializer = ResolveReportSerializer(report, data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['resolve_text'])
            print(serializer.validated_data['resolve_text'])
            report.resolve_text = serializer.validated_data.get("resolve_text")
            report.state = serializer.validated_data.get("state")
            report.resolved_by = request.user
            report.resolved_at = timezone.now()
            report.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

