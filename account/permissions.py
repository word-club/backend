from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # request.user is the performer
    # obj is a model to be compared
    # models has owner in a single form
    # i.e: obj.created_by

    def has_object_permission(self, request, view, obj):
        if obj.created_by:
            return obj.created_by == request.user
        else:
            return False


class IsSuperUser(permissions.BasePermission):
    # request.user is the performer
    def has_permission(self, request, view):
        return request.user.is_superuser
