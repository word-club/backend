from django.urls import path

from report.views import (
    AddCommentReport,
    AddCommunityReport,
    AddPublicationReport,
    AddShareReport,
    AddUserReport,
    ReportDetail,
    ResolveAReport,
    UnResolveAReport,
)

urlpatterns = [
    path("user/<int:pk>/report/", AddUserReport.as_view()),
    path("community/<int:pk>/report/", AddCommunityReport.as_view()),
    path("publication/<int:pk>/report/", AddPublicationReport.as_view()),
    path("comment/<int:pk>/report/", AddCommentReport.as_view()),
    path("share/<int:pk>/report/", AddShareReport.as_view()),
    path("report/<int:pk>/", ReportDetail.as_view()),
    path("report/<int:pk>/resolve/", ResolveAReport.as_view()),
    path("report/<int:pk>/un-resolve/", UnResolveAReport.as_view()),
]
