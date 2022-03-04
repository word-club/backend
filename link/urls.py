from django.urls import path

from link.views import AddCommentLinkView, AddPublicationLinkView, LinkDetail

urlpatterns = [
    path("publication/<int:pk>/link/", AddPublicationLinkView.as_view()),
    path("comment/<int:pk>/link/", AddCommentLinkView.as_view()),
    path("link/<int:pk>/", LinkDetail.as_view()),
]
