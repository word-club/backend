from rest_framework import permissions

from community.models import CommunityAdmin, CommunitySubscription


def check_models(user, community):
    if not community:
        return False
    if not user:
        return False
    return True


class IsCommunityAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj.community if obj.community else obj
        if not check_models(user, community):
            return False

        try:
            CommunityAdmin.objects.get(community=community, user=user)
            return True
        except CommunityAdmin.DoesNotExist:
            return False


class IsSubscriber(permissions.BasePermission):
    # community is obj for request.user to compare with
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        try:
            subscription = CommunitySubscription.objects.get(
                community=community, subscriber=user
            )
            return not subscription.is_banned
        except CommunitySubscription.DoesNotExist:
            return False


class IsApprovedSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        try:
            subscription = CommunitySubscription.objects.get(
                community=community, subscriber=user
            )
            return subscription.is_approved
        except CommunitySubscription.DoesNotExist:
            return False


class IsNotASubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        try:
            CommunitySubscription.objects.get(community=community, subscriber=user)
            return False
        except CommunitySubscription.DoesNotExist:
            return True
