from django.urls import path
from rest_framework.routers import DefaultRouter

from account.views.auth import AdminInspect, LoginView, LogoutView
from account.views.follow import (FollowAUserView, FollowUserViewSet,
                                  UnFollowAUserView)
from account.views.password import (ConfirmResetPassword,
                                    ResetPasswordRequestCode, UpdatePassword)
from account.views.user import (GetMeView, MentionList, ProfileListView,
                                RegisterUserView, RetrieveUserByUsername,
                                UserViewSet)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"follower", FollowUserViewSet, basename="follower")

urlpatterns = router.urls

urlpatterns += [
    path("me/", GetMeView.as_view()),
    path("register/", RegisterUserView.as_view()),
    path("wc-sign-in/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("update-password/", UpdatePassword.as_view(), name="update-password"),
    path(
        "reset-password/",
        ResetPasswordRequestCode.as_view(),
        name="reset-password-request",
    ),
    path(
        "reset-password/<str:code>/",
        ConfirmResetPassword.as_view(),
        name="confirm-reset-password",
    ),
    path("user/<int:pk>/follow/", FollowAUserView.as_view()),
    path("follower/<int:pk>/", UnFollowAUserView.as_view()),
    path("profile/filter/", ProfileListView.as_view({"get": "list"})),
    path("mention-list/", MentionList.as_view()),
    path("user/<str:username>/", RetrieveUserByUsername.as_view()),
    path("user/<str:username>/inspect/", AdminInspect.as_view()),
]
