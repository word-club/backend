from django.urls import path

from bookmark.views import (AddCommentBookmark, AddPublicationBookmark,
                            BookmarkDetail)

urlpatterns = [
    path("publication/<int:pk>/bookmark/", AddPublicationBookmark.as_view()),
    path("publication/<int:pk>/bookmark/", AddCommentBookmark.as_view()),
    path("bookmark/<int:pk>/", BookmarkDetail.as_view()),
]
