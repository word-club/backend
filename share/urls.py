from rest_framework.urls import path

from share.views import AddPublicationShare, AddCommentShare, ShareDetail

urlpatterns = [
    path("publication/<int:pk>/share/", AddPublicationShare.as_view()),
    path("comment/<int:pk>/share/", AddCommentShare.as_view()),
    path("share/<int:pk>/", ShareDetail.as_view()),
]
