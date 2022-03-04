from django.urls import path

from cover.views import AddCommunityCoverView, AddProfileCoverView, CoverDetail

urlpatterns = [
    path("community/<int:pk>/cover/", AddCommunityCoverView.as_view()),
    path("profile/<int:pk>/cover/", AddProfileCoverView.as_view()),
    path("cover/<int:pk>/", CoverDetail.as_view()),
]
