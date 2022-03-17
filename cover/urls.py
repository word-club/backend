from django.urls import path

from cover.views import AddCommunityCoverView, AddProfileCoverView, CoverDetail, ToggleActiveStatus

urlpatterns = [
    path("community/<int:pk>/cover/", AddCommunityCoverView.as_view()),
    path("profile/cover/", AddProfileCoverView.as_view()),
    path("cover/<int:pk>/", CoverDetail.as_view()),
    path("cover/<int:pk>/active/", ToggleActiveStatus.as_view()),
]
