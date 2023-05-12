from rest_framework import permissions

from ban.models import Ban


class IsPublicationAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        instance = obj.publication or obj
        return instance.created_by == request.user


class IsPublished(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_published


class IsNotBanned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not Ban.objects.filter(
            ban_item_app_label="publication",
            ban_item_model="publication",
            ban_item_id=obj.id,
        ).exists()
