from rest_framework.routers import DefaultRouter

from hashtag.views import HashtagViewSet

router = DefaultRouter()

router.register(r"hashtag", HashtagViewSet, basename="hashtag")

urlpatterns = router.urls
