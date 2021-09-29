from rest_framework import permissions

from community.models import CommunityAdmin, CommunitySubscription


def check_models(user, community):
    if not community:
        return False
    if not user:
        return False


class IsCommunityAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False

        community_admins = CommunityAdmin.objects.filter(community=community, user=user)
        return True if user in community_admins else False


class IsSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        community_subscribers = CommunitySubscription.objects.filter(
            community=community
        )
        return True if user in community_subscribers else False


class IsNotASubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        community_subscribers = CommunitySubscription.objects.filter(
            community=community
        )
        return True if user not in community_subscribers else False
