from django.urls import path
from rest_framework.routers import DefaultRouter

from account.views.auth import LoginView, LogoutView
from account.views.follow import FollowUserViewSet, FollowAUserView, UnFollowAUserView
from account.views.password import (
    UpdatePassword,
    ResetPasswordRequestCode,
    ConfirmResetPassword,
)
from account.views.profile import (
    ProfileAvatarViewSet,
    ProfileCoverViewSet,
    AddProfileCoverView,
    AddProfileAvatarView,
)
from account.views.user import RegisterUserView, UserViewSet, DeleteReport, BlockAUser, ReportAUser, UnBlockAUser

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"profile-avatar", ProfileAvatarViewSet, basename="profile-avatar")
router.register(r"profile-cover", ProfileCoverViewSet, basename="profile-cover")
router.register(r"follower", FollowUserViewSet, basename="follower")

urlpatterns = router.urls

urlpatterns += [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginView.as_view(), name="user-login"),
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
    path("profile/<int:pk>/cover/", AddProfileCoverView.as_view()),
    path("profile/<int:pk>/avatar/", AddProfileAvatarView.as_view()),
    path("user/<int:pk>/follow/", FollowAUserView.as_view()),
    path("follower/<int:pk>/", UnFollowAUserView.as_view()),
    path("user/<int:pk>/report/", ReportAUser.as_view()),
    path("user/<int:pk>/block/", BlockAUser.as_view()),
    path("block/<int:pk>/", UnBlockAUser.as_view()),
    path("report/<int:pk>/", DeleteReport.as_view()),

]
