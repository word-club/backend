from rest_framework.routers import DefaultRouter

from hashtag.views import HashtagViewSet

router = DefaultRouter()

router.register(r"hash-tag", HashtagViewSet, basename="hashtag")

urlpatterns = router.urls
