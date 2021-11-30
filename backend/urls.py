"""backend URL Configuration
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.static import serve

from backend.views import TopView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("account.urls")),
    path("api/", include("community.urls")),
    path("api/", include("publication.urls")),
    path("api/", include("comment.urls")),
    path("api/", include("notification.urls")),
    path("api/", include("hashtag.urls")),
    path("api/", include("administration.urls")),
    path("api/top/", TopView.as_view()),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    url(
        r"^robots.txt",
        lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"),
        name="robots_file",
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
