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
    path("publication/<int:pk>/comment/", AddPublicationComment.as_view()),
    path("comment/<int:pk>/", UpdateDestroyCommentView.as_view()),
    path("comment/<int:pk>/up-vote/", UpVoteACommentView.as_view()),
    path("comment/<int:pk>/down-vote/", DownVoteACommentView.as_view()),
    path("comment/<int:pk>/report/", ReportACommentView.as_view()),
    path("comment-report/<int:pk>/", RemoveCommentReportView.as_view()),
    path("comment-image/<int:pk>/", RemoveCommentImageView.as_view()),
    path("comment-image-url/<int:pk>/", RemoveCommentImageUrlView.as_view()),
    path("comment-video-url/<int:pk>/", RemoveCommentVideoUrlView.as_view()),
    path("comment-up-vote/<int:pk>/", RemoveUpVoteForACommentView.as_view()),
    path("comment-down-vote/<int:pk>/", RemoveDownVoteForACommentView.as_view()),
]
