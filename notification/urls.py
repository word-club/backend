from django.urls import path

from notification.views import (
    DestroyNotificationView,
    MyNotificationList,
    SetANotificationAsSeen,
)

urlpatterns = [
    path("me/notifications/", MyNotificationList.as_view()),
    path("notification/<int:pk>/", DestroyNotificationView.as_view()),
    path("notification/<int:pk>/seen/", SetANotificationAsSeen.as_view()),
]
