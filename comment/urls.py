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
    RemoveUpVoteForACommentView,
    RemoveDownVoteForACommentView,
    ReplyCommentView,
    HideCommentForMe,
    BookmarkComment,
    ShareComment,
    RemoveHiddenStatus,
    RemoveCommentBookmark,
    RemoveCommentShare,
    CommentViewSet, CommentPinView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"comment-view", CommentViewSet, basename="comment")
urlpatterns = router.urls

app_name = "comment"

urlpatterns += [
    path("publication/<str:pk>/comment/", AddPublicationComment.as_view()),
    path("comment/<str:pk>/", UpdateDestroyCommentView.as_view()),
    path("comment/<str:pk>/up-vote/", UpVoteACommentView.as_view()),
    path("comment/<str:pk>/down-vote/", DownVoteACommentView.as_view()),
    path("comment/<str:pk>/hide/", HideCommentForMe.as_view()),
    path("comment/<str:pk>/comment/", BookmarkComment.as_view()),
    path("comment/<str:pk>/comment/", ShareComment.as_view()),
    path("comment/<str:pk>/report/", ReportACommentView.as_view()),
    path("comment-report/<str:pk>/", RemoveCommentReportView.as_view()),
    path("comment-image/<str:pk>/", RemoveCommentImageView.as_view()),
    path("comment-image-url/<str:pk>/", RemoveCommentImageUrlView.as_view()),
    path("comment-up-vote/<str:pk>/", RemoveUpVoteForACommentView.as_view()),
    path("comment-down-vote/<str:pk>/", RemoveDownVoteForACommentView.as_view()),
    path("comment/<str:pk>/", UpdateDestroyCommentView.as_view()),
    path("comment/<str:pk>/up-vote/", UpVoteACommentView.as_view()),
    path("comment/<str:pk>/down-vote/", DownVoteACommentView.as_view()),
    path("comment-hide/<str:pk>/", RemoveHiddenStatus.as_view()),
    path("comment-bookmark/<str:pk>/", RemoveCommentBookmark.as_view()),
    path("comment-share/<str:pk>/", RemoveCommentShare.as_view()),
    path("comment/<str:pk>/reply/", ReplyCommentView.as_view()),
    path("comment/<str:pk>/pin/", CommentPinView.as_view()),
]
