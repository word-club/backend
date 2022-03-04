from django.urls import path

from image.views import (AddCommentImageView, AddPublicationImageView,
                         ImageDetail)

urlpatterns = [
    path("comment/<int:pk>/image/", AddCommentImageView.as_view()),
    path("publication/<int:pk>/image/", AddPublicationImageView.as_view()),
    path("image/<int:pk>/", ImageDetail.as_view()),
]
