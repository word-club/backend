from rest_framework import permissions

from community.sub_models.moderator import Moderator


class IsAvatarManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # check if community administrator is the avatar obj has community
        if obj.community:
            return Moderator.objects.filter(community=obj.community, user=request.user).exists()
        # otherwise, the avatar should be for the user profile
        else:
            return obj.profile.created_by.id == request.user.id
