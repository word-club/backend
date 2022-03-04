from django.urls import path
from rest_framework.routers import DefaultRouter

from administration.views import (AdministrationViewSet, PageViewViewSet,
                                  TopView)

router = DefaultRouter()
router.register(r"administration", AdministrationViewSet, basename="administration")
router.register(r"page-view", PageViewViewSet, basename="page-view")
urlpatterns = router.urls

app_name = "administration"

urlpatterns += [
    path("top/", TopView.as_view()),
]
