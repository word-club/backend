from django.urls import path
from rest_framework.routers import DefaultRouter

from community.filters import (CommunitySubscribersFilter,
                               SubscribedCommunityFilter)
from community.views.views import *

router = DefaultRouter()
router.register(r"community-view", CommunityViewSet, basename="community")
urlpatterns = router.urls

app_name = "community"

urlpatterns += [
    path("community/<int:pk>/", CommunityDetail.as_view()),
    path("community/<int:pk>/subscribe/", SubscribeToACommunity.as_view()),
    path(
        "community/<int:pk>/disable-notifications/",
        DisableNotificationsForACommunity.as_view(),
    ),
    path(
        "community/<int:pk>/hashtag/",
        AddCommunityHashtag.as_view(),
    ),
    path(
        "community/<int:pk>/rule/",
        AddCommunityRule.as_view(),
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
        PatchDeleteCommunityRule.as_view(),
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
    path("community/<int:pk>/theme/", AddCommunityTheme.as_view()),
    path("community-theme/<int:pk>/", UpdateCommunityTheme.as_view()),
    path(
        "community-subscriber/<int:pk>/approve/",
        AcceptRejectACommunitySubscriber.as_view(),
    ),
    path("community-subscriber/<int:pk>/ban/", BanUnBanACommunitySubscriber.as_view()),
    path("subscribed-community/filter/", SubscribedCommunityFilter.as_view()),
    path("community/<int:pk>/subscriber-filter/", CommunitySubscribersFilter.as_view()),
    path("top-communities/", TopCommunitiesList.as_view()),
    path("community/<int:pk>/view/", ViewACommunity.as_view()),
]
