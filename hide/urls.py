from django.urls import path

from hide.views import (
    HideAComment,
    HideAPublication,
    HideAUser,
    HideDetail,
)

urlpatterns = [
    path("publication/<int:pk>/hide/", HideAPublication.as_view()),
    path("comment/<int:pk>/hide/", HideAComment.as_view()),
    path("user/<int:pk>/hide/", HideAUser.as_view()),
    path("hide/<int:pk>/", HideDetail.as_view()),
]
