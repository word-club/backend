from community.models import Subscription
from notification.models import Notification, NotificationTo


def check_community_law(community, user):
    if community:
        try:
            subscriber = Subscription.objects.get(created_by=user, community=community)
            if subscriber.is_banned:
                return True, {"detail": "Subscriber is banned for the selected community."}
            if community.type != "public":
                if not subscriber.is_approved:
                    return True, {"detail": "Subscriber is not approved yet."}
            return False, None
        except Subscription.DoesNotExist:
            return True, {"detail": "Please subscribe the community first to add publication."}


def send_notification(receivers, notification, threshold=1):
    # more than one because, the first admin is the author
    if receivers and receivers.count() > threshold:
        [
            NotificationTo.objects.create(user=receiver.user, notification=notification)
            for receiver in receivers
        ]


def notify_community(instance, created):
    # TODO: if subscription, notify community admin, sub admin
    if instance.__class__.__name__ == "Subscription":
        notification = Notification.objects.create(
            subject="subscription", community=instance.community, subscription=instance
        )
        admins = instance.community.moderators
        send_notification(admins, notification)
        sub_admins = instance.community.sub_moderators
        send_notification(sub_admins, notification)
    pass
