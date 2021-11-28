from community.models import CommunitySubscription


def check_community_law(community, user):
    if community:
        try:
            subscriber = CommunitySubscription.objects.get(
                subscriber=user, community=community
            )
            if subscriber.is_banned:
                return True, {
                    "detail": "Subscriber is banned for the selected community."
                }
            if community.type != "public":
                if not subscriber.is_approved:
                    return True, {"detail": "Subscriber is not approved yet."}
            return False, None
        except CommunitySubscription.DoesNotExist:
            return True, {
                "detail": "Please subscribe the community first to add publication."
            }
