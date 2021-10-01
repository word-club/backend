from django.urls import path
from rest_framework.routers import DefaultRouter

from publication.views import (
    PublicationListRetrieveView, AddPublicationHashtag, RemovePublicationHashtag,
    AddPublicationImageView, RemovePublicationImageView, AddPublicationImageUrlView, RemovePublicationImageUrlView,
    UpVoteAPublicationView, RemovePublicationUpVote, DownVoteAPublication, BookmarkAPublicationView,
    RemovePublicationDownVote, RemovePublicationBookmarkView, HideAPublicationView, RemovePublicationHiddenStateView,
    ReportAPublicationView, RemovePublicationReportView, AddPublicationView, UpdatePublicationView,
)

router = DefaultRouter()
router.register(r"s/publication", PublicationListRetrieveView, basename="publication-list-retrieve")

urlpatterns = router.urls

urlpatterns += [
    path('publication/', AddPublicationView.as_view()),
    path('publication/<str:pk>/', UpdatePublicationView.as_view()),
    path('publication/<str:pk>/tag/', AddPublicationHashtag.as_view()),
    path('publication-tag/<str:pk>/', RemovePublicationHashtag.as_view()),
    path('publication/<str:pk>/image/', AddPublicationImageView.as_view()),
    path('publication-imgage/<str:pk>/', RemovePublicationImageView.as_view()),
    path('publication/<str:pk>/image-url/', AddPublicationImageUrlView.as_view()),
    path('publication-image-url/<str:pk>/', RemovePublicationImageUrlView.as_view()),
    path('publication/<str:pk>/up-vote/', UpVoteAPublicationView.as_view()),
    path('publication-up-vote/<str:pk>/', RemovePublicationUpVote.as_view()),
    path('publication/<str:pk>/down-vote/', DownVoteAPublication.as_view()),
    path('publication-down-vote/<str:pk>/', RemovePublicationDownVote.as_view()),
    path('publication/<str:pk>/bookmark/', BookmarkAPublicationView.as_view()),
    path('publication-bookmark/<str:pk>/', RemovePublicationBookmarkView.as_view()),
    path('publication/<str:pk>/hide/', HideAPublicationView.as_view()),
    path('publication-hide/<str:pk>/', RemovePublicationHiddenStateView.as_view()),
    path('publication/<str:pk>/report/', ReportAPublicationView.as_view()),
    path('publication-report/<str:pk>/', RemovePublicationReportView.as_view()),
]
