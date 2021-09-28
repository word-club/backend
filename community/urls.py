from django.urls import path
from rest_framework.routers import DefaultRouter

from community.views import *

router = DefaultRouter()
router.register(r"community", CommunityViewSet, basename="community")
urlpatterns = router.urls

urlpatterns += [
    path("community/<str:pk>/report", ReportACommunity.as_view()),
    path("community/<str:pk>/subscribe", SubscribeToACommunity.as_view()),
    path(
        "community/<str:pk>/disable-notifications",
        DisableNotificationsForACommunity.as_view(),
    ),
    path(
        "community/<str:pk>/avatar",
        AddCommunityAvatar.as_view(),
    ),
    path(
        "community/<str:pk>/cover",
        AddCommunityCover.as_view(),
    ),
    path(
        "disable-notifications/<int:pk>",
        RemoveCommunityDisableNotification.as_view(),
    ),
    path(
        "community-rule/<int:pk>",
        DeleteCommunityRule.as_view(),
    ),
    path(
        "community-cover/<int:pk>",
        DeleteCommunityCover.as_view(),
    ),
    path(
        "community-avatar/<int:pk>",
        DeleteCommunityAvatar.as_view(),
    ),
    path(
        "community-report/<int:pk>",
        DeleteCommunityReport.as_view(),
    ),
    path(
        "community-unsubscribe/<int:pk>",
        RemoveCommunityDisableNotification.as_view(),
    ),
    path(
        "community-avatar/<int:pk>/set-active",
        SetActiveCommunityAvatar.as_view(),
    ),
    path(
        "community-cover/<int:pk>/set-active",
        SetActiveCommunityCover.as_view(),
    ),
]
