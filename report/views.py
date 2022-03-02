from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404

from account.permissions import IsOwner, IsSuperUser
from comment.models import Comment
from community.models import Community
from publication.models import Publication
from report.models import Report
from report.serializers import ReportSerializer, ResolveReportSerializer


class AddUserReport(APIView):
    """
    Add a user report to the database.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        context = {
            "user": user,
            "request": request,
        }
        serializer = ReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommunityReport(APIView):
    """
    Add a community report to the database.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        context = {
            "community": community,
            "request": request,
        }
        serializer = ReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPublicationReport(APIView):
    """
    Add a publication report to the database.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        context = {
            "publication": publication,
            "request": request,
        }
        serializer = ReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentReport(APIView):
    """
    Add a comment report to the database.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        context = {
            "comment": comment,
            "request": request,
        }
        serializer = ReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddShareReport(APIView):
    """
    Add a share report to the database.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        share = get_object_or_404(Comment, pk=pk)
        context = {
            "share": share,
            "request": request,
        }
        serializer = ReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetail(APIView):
    """
    Delete a report from the database.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        self.check_object_permissions(request, report)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def patch(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        self.check_object_permissions(request, report)
        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResolveAReport(APIView):
    """
    Resolve a report from the database.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        self.check_object_permissions(request, report)

        if not report.is_pending:
            return Response(
                {"detail": "Report is already resolved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ResolveReportSerializer(report, data=request.data)
        if serializer.is_valid():
            report.resolve_text = serializer.validated_data.get("resolve_text")
            report.state = serializer.validated_data.get("state")
            report.resolved_by = request.user
            report.resolved_at = timezone.now()
            report.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnResolveAReport(APIView):
    """
    Unresolve a report from the database.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        self.check_object_permissions(request, report)

        if report.is_pending:
            return Response(
                {"detail": "This report is not resolved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report.resolve_text = None
        report.state = "pending"
        report.resolved_by = None
        report.resolved_at = None
        report.save()
        return Response(status=status.HTTP_200_OK)
