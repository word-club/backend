from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # request.user is the performer
    # obj is a model to be compared
    # models has owner in two form
    # i.e: obj.user for NotificationTo model
    # and: obj.created_by for all others

    def has_object_permission(self, request, view, obj):
        if obj.created_by:
            return obj.created_by == request.user
        elif obj.user:
            return obj.user == request.user
        else:
            return False


class IsSuperUser(permissions.BasePermission):
    # request.user is the performer
    def has_permission(self, request, view):
        return request.user.is_superuser
