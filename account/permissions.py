from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.profile:
            return obj.profile.user == request.user
        elif obj.user:
            return obj.user == request.user
        else:
            return False
