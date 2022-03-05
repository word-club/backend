from rest_framework import permissions


class IsPublicationAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        instance = obj.publication or obj
        return instance.created_by == request.user


class IsPublished(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_published
