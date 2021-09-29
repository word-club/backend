from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.profile:  # for profile items
            return obj.profile.user == request.user
        elif obj.user:  # for profile
            return obj.user == request.user
        elif obj.created_by:  # for other models
            return obj.created_by == request.user
        else:
            return False
