from django.urls import path
from rest_framework.routers import DefaultRouter

from comment.filter import CommentFilter
from comment.views import (AddPublicationComment, CommentDetail,
                           CommentPinView, CommentViewSet, ReplyCommentView)

router = DefaultRouter()
router.register(r"comment-view", CommentViewSet, basename="comment")
urlpatterns = router.urls

app_name = "comment"

urlpatterns += [
    path("publication/<str:pk>/comment/", AddPublicationComment.as_view()),
    path("comment/<str:pk>/", CommentDetail.as_view()),
    path("comment/<str:pk>/reply/", ReplyCommentView.as_view()),
    path("comment/<str:pk>/pin/", CommentPinView.as_view()),
    path("comment-filter/", CommentFilter.as_view()),
]
