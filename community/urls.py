from django.urls import path
from rest_framework.routers import DefaultRouter

from community.views import *

router = DefaultRouter()
router.register(r"community", CommunityViewSet, basename="community")
urlpatterns = router.urls

urlpatterns += [
    path("community/<int:pk>/report/", ReportACommunity.as_view()),
    path("community/<int:pk>/subscribe/", SubscribeToACommunity.as_view()),
    path(
        "community/<int:pk>/disable-notifications/",
        DisableNotificationsForACommunity.as_view(),
    ),
    path(
        "community/<int:pk>/avatar/",
        AddCommunityAvatar.as_view(),
    ),
    path(
        "community/<int:pk>/cover/",
        AddCommunityCover.as_view(),
    ),
    path(
        "community/<int:pk>/hashtag/",
        AddCommunityHashtag.as_view(),
    ),
    path(
        "community/<int:pk>/admin/",
        AddCommunityAdmin.as_view(),
    ),
    path(
        "disable-notifications/<int:pk>/",
        RemoveCommunityDisableNotification.as_view(),
    ),
    path(
        "community-rule/<int:pk>/",
        DeleteCommunityRule.as_view(),
    ),
    path(
        "community-cover/<int:pk>/",
        DeleteCommunityCover.as_view(),
    ),
    path(
        "community-avatar/<int:pk>/",
        DeleteCommunityAvatar.as_view(),
    ),
    path(
        "community-report/<int:pk>/",
        DeleteCommunityReport.as_view(),
    ),
    path(
        "community-unsubscribe/<int:pk>/",
        UnSubscribeCommunity.as_view(),
    ),
    path(
        "community-hashtag/<int:pk>/",
        RemoveCommunityHashtag.as_view(),
    ),
    path(
        "community-admin/<int:pk>/",
        RemoveCommunityAdmin.as_view(),
    ),
    path(
        "authorize-community/<int:pk>/request",
        RequestCommunityAuthorization.as_view(),
        name="authorize-community",
    ),
    path(
        "authorize-community/<str:pk>/confirm",
        ConfirmCommunityAuthorization.as_view,
        name="confirm-authorize-community",
    ),
]
