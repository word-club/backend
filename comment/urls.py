from django.urls import path

from comment.views import (
    AddPublicationComment,
    UpdateDestroyCommentView,
    UpVoteACommentView,
    DownVoteACommentView,
    ReportACommentView,
    RemoveCommentReportView,
    RemoveCommentImageView,
    RemoveCommentImageUrlView,
    RemoveCommentVideoUrlView,
    RemoveUpVoteForACommentView,
    RemoveDownVoteForACommentView,
)

urlpatterns = [
    path("publication/<str:pk>/comment/", AddPublicationComment.as_view()),
    path("comment/<str:pk>/", UpdateDestroyCommentView.as_view()),
    path("comment/<str:pk>/up-vote/", UpVoteACommentView.as_view()),
    path("comment/<str:pk>/down-vote/", DownVoteACommentView.as_view()),
    path("comment/<str:pk>/report/", ReportACommentView.as_view()),
    path("comment-report/<str:pk>/", RemoveCommentReportView.as_view()),
    path("comment-image/<str:pk>/", RemoveCommentImageView.as_view()),
    path("comment-image-url/<str:pk>/", RemoveCommentImageUrlView.as_view()),
    path("comment-video-url/<str:pk>/", RemoveCommentVideoUrlView.as_view()),
    path("comment-up-vote/<str:pk>/", RemoveUpVoteForACommentView.as_view()),
    path("comment-down-vote/<str:pk>/", RemoveDownVoteForACommentView.as_view()),
]
