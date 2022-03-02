from rest_framework.urls import path

from vote.views import (
    AddPublicationUpVote,
    AddPublicationDownVote,
    AddCommentUpVote,
    AddCommentDownVote,
    DestroyVote
)

urlpatterns = [
    path('publication/<int:pk>/up-vote/', AddPublicationUpVote.as_view()),
    path('publication/<int:pk>/down-vote/', AddPublicationDownVote.as_view()),
    path('comment/<int:pk>/up-vote/', AddCommentUpVote.as_view()),
    path('comment/<int:pk>/down-vote/', AddCommentDownVote.as_view()),
    path('vote/<int:pk>/', DestroyVote.as_view())
]
