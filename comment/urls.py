from django.urls import path
from rest_framework.routers import DefaultRouter

from comment.filter import CommentFilter
from comment.views import (
    AddPublicationComment,
    CommentDetail,
    CommentPinView,
    CommentViewSet,
    ReplyCommentView,
)

router = DefaultRouter()
router.register(r"wc-comment", CommentViewSet, basename="comment")
urlpatterns = router.urls

app_name = "comment"

urlpatterns += [
    path("publication/<int:pk>/comment/", AddPublicationComment.as_view()),
    path("comment/<int:pk>/", CommentDetail.as_view()),
    path("comment/<int:pk>/reply/", ReplyCommentView.as_view()),
    path("comment/<int:pk>/pin/", CommentPinView.as_view()),
    path("comment/filter/", CommentFilter.as_view()),
]
