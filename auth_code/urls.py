from django.urls import path

from auth_code.views import (
    ConfirmCommunityAuthorization,
    ConfirmResetPassword,
    ConfirmUserAuthorization,
    RequestCommunityAuthorization,
    RequestUserAuthorization,
    ResetPasswordRequestCode,
)

urlpatterns = [
    path(
        "reset-password/",
        ResetPasswordRequestCode.as_view(),
        name="reset-password-request",
    ),
    path(
        "reset-password/<str:code>/",
        ConfirmResetPassword.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "authorize-community/<int:pk>/request/",
        RequestCommunityAuthorization.as_view(),
        name="authorize-community",
    ),
    path(
        "authorize-user/<int:pk>/request/",
        RequestUserAuthorization.as_view(),
        name="authorize-user",
    ),
    path(
        "authorize-community/<str:code>/confirm/",
        ConfirmCommunityAuthorization.as_view(),
        name="confirm-authorize-community",
    ),
    path(
        "authorize-user/<str:code>/confirm/",
        ConfirmUserAuthorization.as_view(),
        name="confirm-authorize-user",
    ),
]
