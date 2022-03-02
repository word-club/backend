from django.urls import path
from rest_framework.routers import DefaultRouter

from publication.filter import PublicationFilter
from publication.views import (
    PublicationListView,
    AddPublicationImageView,
    RemovePublicationImageView,
    AddPublicationImageUrlView,
    RemovePublicationImageUrlView,
    BookmarkAPublicationView,
    RemovePublicationBookmarkView,
    HideAPublicationView,
    RemovePublicationHiddenStateView,
    AddPublicationView,
    RetrieveUpdatePublicationView,
    PublishPublicationView,
    EditOrRemovePublicationLink,
    AddPublicationLinkView,
    GetTwitterEmbed,
    PublicationPinView,
    ViewAPublication,
)

router = DefaultRouter()
router.register(r"s/publication", PublicationListView, basename="publication-list")

urlpatterns = router.urls

urlpatterns += [
    path("publication/", AddPublicationView.as_view()),
    path("publication/<int:pk>/", RetrieveUpdatePublicationView.as_view()),
    path("publication/<int:pk>/publish/", PublishPublicationView.as_view()),
    path("publication/<int:pk>/image/", AddPublicationImageView.as_view()),
    path("publication-image/<int:pk>/", RemovePublicationImageView.as_view()),
    path("publication/<int:pk>/image-url/", AddPublicationImageUrlView.as_view()),
    path("publication-image-url/<int:pk>/", RemovePublicationImageUrlView.as_view()),
    path("publication/<int:pk>/bookmark/", BookmarkAPublicationView.as_view()),
    path("publication-bookmark/<int:pk>/", RemovePublicationBookmarkView.as_view()),
    path("publication/<int:pk>/hide/", HideAPublicationView.as_view()),
    path("publication-hide/<int:pk>/", RemovePublicationHiddenStateView.as_view()),
    path("publication/<int:pk>/link/", AddPublicationLinkView.as_view()),
    path("publication-link/<int:pk>/", EditOrRemovePublicationLink.as_view()),
    path("get-twitter-embed/", GetTwitterEmbed.as_view()),
    path("publication/<int:pk>/pin/", PublicationPinView.as_view()),
    path("publication/filter/", PublicationFilter.as_view()),
    path("publication/<int:pk>/view/", ViewAPublication.as_view()),
]
