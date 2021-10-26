from django.urls import path
from rest_framework.routers import DefaultRouter

from publication.views import (
    PublicationListRetrieveView,
    AddPublicationHashtag,
    RemovePublicationHashtag,
    AddPublicationImageView,
    RemovePublicationImageView,
    AddPublicationImageUrlView,
    RemovePublicationImageUrlView,
    UpVoteAPublicationView,
    RemovePublicationUpVote,
    DownVoteAPublication,
    BookmarkAPublicationView,
    RemovePublicationDownVote,
    RemovePublicationBookmarkView,
    HideAPublicationView,
    RemovePublicationHiddenStateView,
    ReportAPublicationView,
    RemovePublicationReportView,
    AddPublicationView,
    UpdatePublicationView,
    PublishPublicationView,
    EditOrRemovePublicationLink,
    AddPublicationLinkView,
)

router = DefaultRouter()
router.register(
    r"s/publication", PublicationListRetrieveView, basename="publication-list-retrieve"
)

urlpatterns = router.urls

urlpatterns += [
    path("publication/", AddPublicationView.as_view()),
    path("publication/<int:pk>/", UpdatePublicationView.as_view()),
    path("publication/<int:pk>/publish/", PublishPublicationView.as_view()),
    path("publication/<int:pk>/tag/", AddPublicationHashtag.as_view()),
    path("publication-tag/<int:pk>/", RemovePublicationHashtag.as_view()),
    path("publication/<int:pk>/image/", AddPublicationImageView.as_view()),
    path("publication-imgage/<int:pk>/", RemovePublicationImageView.as_view()),
    path("publication/<int:pk>/image-url/", AddPublicationImageUrlView.as_view()),
    path("publication-image-url/<int:pk>/", RemovePublicationImageUrlView.as_view()),
    path("publication/<int:pk>/up-vote/", UpVoteAPublicationView.as_view()),
    path("publication-up-vote/<int:pk>/", RemovePublicationUpVote.as_view()),
    path("publication/<int:pk>/down-vote/", DownVoteAPublication.as_view()),
    path("publication-down-vote/<int:pk>/", RemovePublicationDownVote.as_view()),
    path("publication/<int:pk>/bookmark/", BookmarkAPublicationView.as_view()),
    path("publication-bookmark/<int:pk>/", RemovePublicationBookmarkView.as_view()),
    path("publication/<int:pk>/hide/", HideAPublicationView.as_view()),
    path("publication-hide/<int:pk>/", RemovePublicationHiddenStateView.as_view()),
    path("publication/<int:pk>/report/", ReportAPublicationView.as_view()),
    path("publication-report/<int:pk>/", RemovePublicationReportView.as_view()),
    path("publication/<int:pk>/link/", AddPublicationLinkView.as_view()),
    path("publication-link/<int:pk>/", EditOrRemovePublicationLink.as_view()),
]
