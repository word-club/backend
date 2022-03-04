from django.urls import path
from rest_framework.routers import DefaultRouter

from publication.filter import PublicationFilter
from publication.views import (
    PublicationListView,
    AddPublicationView,
    RetrieveUpdatePublicationView,
    PublishPublicationView,
    GetTwitterEmbed,
    PublicationPinView,
    ViewAPublication,
)

router = DefaultRouter()
router.register(r"s/publication", PublicationListView, basename="publication-list")

urlpatterns = router.urls

urlpatterns += [
    path("publication/", AddPublicationView.as_view()),
    path("publication/<int:pk>/", RetrieveUpdatePublicationView.as_view()),
    path("publication/<int:pk>/publish/", PublishPublicationView.as_view()),
    path("get-twitter-embed/", GetTwitterEmbed.as_view()),
    path("publication/<int:pk>/pin/", PublicationPinView.as_view()),
    path("publication/filter/", PublicationFilter.as_view()),
    path("publication/<int:pk>/view/", ViewAPublication.as_view()),
]
