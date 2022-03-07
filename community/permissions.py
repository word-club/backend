from rest_framework import permissions

from community.models import Moderator, Subscription


def check_models(user, community):
    if not community:
        return False
    if not user:
        return False
    return True


class IsCommunityModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            community = obj.community
        except AttributeError:
            community = obj
        if not check_models(user, community):
            return False

        try:
            Moderator.objects.get(community=community, user=user, role="mod")
            return True
        except Moderator.DoesNotExist:
            return False


class IsSubscriber(permissions.BasePermission):
    # community is obj for request.user to compare with
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        try:
            subscription = Subscription.objects.get(community=community, subscriber=user)
            return not subscription.is_banned
        except Subscription.DoesNotExist:
            return False


class IsApprovedSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        try:
            subscription = Subscription.objects.get(community=community, subscriber=user)
            return subscription.is_approved
        except Subscription.DoesNotExist:
            return False


class IsNotASubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        community = obj
        if not check_models(user, community):
            return False
        try:
            Subscription.objects.get(community=community, subscriber=user)
            return False
        except Subscription.DoesNotExist:
            return True


class IsNotBannedSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.__class__.__name__ == "AnonymousUser":
            return True
        community = obj
        if not check_models(user, community):
            return False
        try:
            subscription = Subscription.objects.get(community=community, subscriber=user)
            return not subscription.is_banned
        except Subscription.DoesNotExist:
            return True
