from django.urls import path
from rest_framework.routers import DefaultRouter

from community.filters import (
    CommunitySubscribersFilter,
    SubscribedCommunityFilter,
    TopCommunitiesList,
    TrendingCommunityList,
)
from community.views.community import CommunityDetail, CommunityViewSet, ViewACommunity
from community.views.hashtag import UpdateCommunityHashtag
from community.views.moderator import AddModerator, AddSubModerator, ModeratorDetail
from community.views.rule import AddCommunityRule, PatchDeleteCommunityRule
from community.views.subscription import (
    AcceptRejectASubscriber,
    BanUnBanASubscriber,
    DisableNotifications,
    RemoveDisableNotification,
    SubscribeToACommunity,
    SubscriptionDetail,
)
from community.views.theme import UpdateCommunityTheme

router = DefaultRouter()
router.register(r"wc-community", CommunityViewSet, basename="community")
urlpatterns = router.urls

app_name = "community"

urlpatterns += [
    path("community/<int:pk>/", CommunityDetail.as_view()),
    path("community/top/", TopCommunitiesList.as_view()),
    path("community/trending/", TrendingCommunityList.as_view()),
    path("community/<str:unique_id>/view/", ViewACommunity.as_view()),
    path("community/<int:pk>/subscriber/filter/", CommunitySubscribersFilter.as_view()),
    path("community/<int:pk>/subscribe/", SubscribeToACommunity.as_view()),
    path("subscriber/<int:pk>/approve/", AcceptRejectASubscriber.as_view()),
    path("subscriber/<int:pk>/ban/", BanUnBanASubscriber.as_view()),
    path("subscription/filter/", SubscribedCommunityFilter.as_view()),
    path("subscription/<int:pk>/disable-notifications/", DisableNotifications.as_view()),
    path("subscription/<int:pk>/enable-notifications/", RemoveDisableNotification.as_view()),
    path("subscription/<int:pk>/", SubscriptionDetail.as_view()),
    path("community/<int:pk>/hashtag/", UpdateCommunityHashtag.as_view()),
    path("community/<int:pk>/rule/", AddCommunityRule.as_view()),
    path("community/<int:pk>/mod/", AddModerator.as_view()),
    path("community/<int:pk>/sub-mod/", AddSubModerator.as_view()),
    path("community/rule/<int:pk>/", PatchDeleteCommunityRule.as_view()),
    path("community/moderator/<int:pk>/", ModeratorDetail.as_view()),
    path("community/theme/<int:pk>/", UpdateCommunityTheme.as_view()),
]
