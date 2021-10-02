from django.urls import path

from notification.views import NotificationListCreateView

urlpatterns = [
    path("notification/", NotificationListCreateView.as_view())
]
