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
        "community/<str:pk>/hashtag",
        AddCommunityHashtag.as_view(),
    ),
    path(
        "community/<str:pk>/admin",
        AddCommunityAdmin.as_view(),
    ),
    path(
        "disable-notifications/<str:pk>",
        RemoveCommunityDisableNotification.as_view(),
    ),
    path(
        "community-rule/<str:pk>",
        DeleteCommunityRule.as_view(),
    ),
    path(
        "community-cover/<str:pk>",
        DeleteCommunityCover.as_view(),
    ),
    path(
        "community-avatar/<str:pk>",
        DeleteCommunityAvatar.as_view(),
    ),
    path(
        "community-report/<str:pk>",
        DeleteCommunityReport.as_view(),
    ),
    path(
        "community-unsubscribe/<str:pk>",
        RemoveCommunityDisableNotification.as_view(),
    ),
    path(
        "community-hashtag/<str:pk>",
        RemoveCommunityHashtag.as_view(),
    ),
    path(
        "community-avatar/<str:pk>/set-active",
        SetActiveCommunityAvatar.as_view(),
    ),
    path(
        "community-cover/<str:pk>/set-active",
        SetActiveCommunityCover.as_view(),
    ),
    path(
        "community-admin/<str:pk>/admin",
        RemoveCommunityAdmin.as_view(),
    ),
]
