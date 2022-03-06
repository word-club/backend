from django.urls import path
from rest_framework.routers import DefaultRouter

from account.views.auth import AdminInspect, LoginView, LogoutView
from account.views.follow import FollowAUserView, UnFollowAUserView
from account.views.mention import MentionList
from account.views.password import UpdatePassword
from account.views.user import (
    GetMeView,
    ProfileListView,
    RegisterUserView,
    RetrieveUserByUsername,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = router.urls

urlpatterns += [
    path("me/", GetMeView.as_view()),
    path("wc-register/", RegisterUserView.as_view()),
    path("wc-signin/", LoginView.as_view(), name="user-login"),
    path("wc-signout/", LogoutView.as_view(), name="user-logout"),
    path("update-password/", UpdatePassword.as_view(), name="update-password"),
    path("user/<int:pk>/follow/", FollowAUserView.as_view()),
    path("follower/<int:pk>/", UnFollowAUserView.as_view()),
    path("profile/filter/", ProfileListView.as_view({"get": "list"})),
    path("mention-list/", MentionList.as_view()),
    path("user/<str:username>/", RetrieveUserByUsername.as_view()),
    path("user/<str:username>/inspect/", AdminInspect.as_view()),
]
