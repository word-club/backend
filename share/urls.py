from rest_framework.urls import path

from share.views import AddCommentShare, AddPublicationShare, ShareDetail, ShareList

urlpatterns = [
    path("publication/<int:pk>/share/", AddPublicationShare.as_view()),
    path("comment/<int:pk>/share/", AddCommentShare.as_view()),
    path("share/<int:pk>/", ShareDetail.as_view()),
    path("share/", ShareList.as_view()),
]
