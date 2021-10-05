from rest_framework import permissions


class IsPublicationAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.publication:
            return False
        return obj.publication.created_by == request.user
