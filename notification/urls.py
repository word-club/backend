from django.urls import path

from notification.views import (
    NotificationListCreateView,
    DestroyNotificationView,
    SetANotificationAsSeen,
)

urlpatterns = [
    path("notification/", NotificationListCreateView.as_view()),
    path("notification/<int:pk>", DestroyNotificationView.as_view()),
    path("notification/<int:pk>/seen", SetANotificationAsSeen.as_view()),
]
