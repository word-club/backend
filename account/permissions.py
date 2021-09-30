from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # request.user is performer
    # obj is a model to be compared
    # models has owner in different forms:
    # profile -> for profile related models
    # user -> for profile model
    # created_by -> every other model

    def has_object_permission(self, request, view, obj):
        if obj.created_by: return obj.created_by == request.user
        elif obj.user: return obj.user == request.user
        elif obj.profile: return obj.profile.user == request.user
        else: return False


class IsSuperUser(permissions.BasePermission):
    # request.user is performer

    def has_permission(self, request, view):
        return request.user.is_superuser
