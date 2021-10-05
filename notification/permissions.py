from rest_framework import permissions

from notification.models import NotificationTo


class IsGlobalNotification(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        notification = obj.notification if obj.notification else obj
        return notification.is_global


class IsNotificationReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        notification = obj.notification if obj.notification else obj
        receivers = NotificationTo.objects.filter(notification=notification)
        for receiver in receivers:
            if receiver.user == request.user:
                return True
        return False
