from django.urls import path

from bookmark.views import (
    AddCommentBookmark,
    AddCommunityBookmark,
    AddPublicationBookmark,
    BookmarkDetail, BookmarkList
)

urlpatterns = [
    path("publication/<int:pk>/bookmark/", AddPublicationBookmark.as_view()),
    path("community/<int:pk>/bookmark/", AddCommunityBookmark.as_view()),
    path("comment/<int:pk>/bookmark/", AddCommentBookmark.as_view()),
    path("bookmark/<int:pk>/", BookmarkDetail.as_view()),
    path("bookmark/", BookmarkList.as_view()),
]
