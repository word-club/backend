from django.urls import path
from rest_framework.routers import DefaultRouter

from publication.filter import PublicationFilter
from publication.views import (
    ListPublicationView,
    AddPublicationView,
    PublicationListView,
    PublicationPinView,
    PublishPublicationView,
    RetrieveUpdatePublicationView,
    GetAPublication,
    RecentPublicationView,
)

router = DefaultRouter()
router.register(r"wc-publication", PublicationListView, basename="publication-list")

urlpatterns = router.urls

urlpatterns += [
    path("publication-list/", ListPublicationView.as_view()),
    path("publication/", AddPublicationView.as_view()),
    path("publication/<int:pk>/", RetrieveUpdatePublicationView.as_view()),
    path("publication/<int:pk>/publish/", PublishPublicationView.as_view()),
    path("publication/<int:pk>/pin/", PublicationPinView.as_view()),
    path("publication/filter/", PublicationFilter.as_view()),
    path("publication/<int:pk>/view/", GetAPublication.as_view()),
    path("publication/<int:pk>/recent/", RecentPublicationView.as_view()),
]
