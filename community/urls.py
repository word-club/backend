from django.urls import path
from rest_framework.routers import DefaultRouter

from community.filters import (CommunitySubscribersFilter,
                               SubscribedCommunityFilter, TopCommunitiesList)
from community.views.community import (CommunityDetail, CommunityViewSet,
                                       ViewACommunity)
from community.views.hashtag import UpdateCommunityHashtag
from community.views.moderator import (AddModerator, AddSubModerator,
                                       ModeratorDetail)
from community.views.rule import AddCommunityRule, PatchDeleteCommunityRule
from community.views.subscription import (AcceptRejectACommunitySubscriber,
                                          BanUnBanACommunitySubscriber,
                                          DisableNotificationsForACommunity,
                                          RemoveCommunityDisableNotification,
                                          SubscribeToACommunity,
                                          SubscriptionDetail)
from community.views.theme import AddCommunityTheme, UpdateCommunityTheme

router = DefaultRouter()
router.register(r"wc-community", CommunityViewSet, basename="community")
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
        UpdateCommunityHashtag.as_view(),
    ),
    path(
        "community/<int:pk>/rule/",
        AddCommunityRule.as_view(),
    ),
    path(
        "community/<int:pk>/mod/",
        AddModerator.as_view(),
    ),
    path(
        "community/<int:pk>/sub-mod/",
        AddSubModerator.as_view(),
    ),
    path(
        "notifications/<int:pk>/disable/",
        RemoveCommunityDisableNotification.as_view(),
    ),
    path(
        "rule/<int:pk>/",
        PatchDeleteCommunityRule.as_view(),
    ),
    path(
        "subscription/<int:pk>/",
        SubscriptionDetail.as_view(),
    ),
    path(
        "moderator/<int:pk>/",
        ModeratorDetail.as_view(),
    ),
    path("community/<int:pk>/theme/", AddCommunityTheme.as_view()),
    path("community-theme/<int:pk>/", UpdateCommunityTheme.as_view()),
    path(
        "subscriber/<int:pk>/approve/",
        AcceptRejectACommunitySubscriber.as_view(),
    ),
    path("subscriber/<int:pk>/ban/", BanUnBanACommunitySubscriber.as_view()),
    path("subscribed-community/filter/", SubscribedCommunityFilter.as_view()),
    path("community/<int:pk>/subscriber-filter/", CommunitySubscribersFilter.as_view()),
    path("top-communities/", TopCommunitiesList.as_view()),
    path("community/<int:pk>/view/", ViewACommunity.as_view()),
]
