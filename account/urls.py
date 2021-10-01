from django.urls import path
from rest_framework.routers import DefaultRouter

from account.views.auth import LoginView, LogoutView
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
    SetActiveProfileAvatarView,
    SetActiveProfileCoverView,
)
from account.views.user import RegisterUserView, UserViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"profile-avatar", ProfileAvatarViewSet, basename="profile-avatar")
router.register(r"profile-cover", ProfileCoverViewSet, basename="profile-cover")

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
    path("profile/<str:pk>/cover/", AddProfileCoverView.as_view()),
    path("profile/<str:pk>/avatar/", AddProfileAvatarView.as_view()),
    path("profile-cover/<int:pk>/set-active/", SetActiveProfileCoverView.as_view()),
    path("profile-avatar/<int:pk>/set-active/", SetActiveProfileAvatarView.as_view()),
]
