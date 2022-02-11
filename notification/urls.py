from django.urls import path

from notification.views import (
    DestroyNotificationView,
    SetANotificationAsSeen,
    NotificationListView,
)

urlpatterns = [
    path("notification/", NotificationListView.as_view()),
    path("notification/<int:pk>", DestroyNotificationView.as_view()),
    path("notification/<int:pk>/mark-seen", SetANotificationAsSeen.as_view()),
]
