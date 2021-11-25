from rest_framework.routers import DefaultRouter

from administration.views import AdministrationViewSet, PageViewViewSet

router = DefaultRouter()
router.register(r"administration", AdministrationViewSet, basename="administration")
router.register(r"page-view", PageViewViewSet, basename="page-view")
urlpatterns = router.urls

app_name = "administration"
