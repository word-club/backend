from notification.models import Notification, NotificationTo


def add_popularity(trigger):
    instance = trigger.publication or trigger.comment
    instance.popularity += 1
    instance.save()
    instance.created_by.profile.popularity += 1
    instance.created_by.profile.save()
    if hasattr(instance, "community") and instance.community:
        instance.community.popularity += 1
        instance.community.save()


def add_supports(vote):
    instance = vote.publication or vote.comment
    instance.supports += 1
    instance.save()
    instance.created_by.profile.supports += 1
    instance.created_by.profile.save()
    if hasattr(instance, "community") and instance.community:
        instance.community.supports += 1
        instance.community.save()


def add_dislikes(vote):
    instance = vote.publication or vote.comment
    instance.dislikes += 1
    instance.save()
    instance.created_by.profile.dislikes += 1
    instance.created_by.profile.save()
    if hasattr(instance, "community") and instance.community:
        instance.community.dislikes += 1
        instance.community.save()


def decrease_popularity(vote):
    instance = vote.publication or vote.comment
    if instance.popularity > 0:
        instance.popularity -= 1
        instance.save()
    if instance.created_by.profile.popularity > 0:
        instance.created_by.profile.popularity -= 1
        instance.created_by.profile.save()
    if hasattr(instance, "community") and instance.community and instance.community.popularity > 0:
        instance.community.popularity -= 1
        instance.community.save()


def decrease_dislikes(vote):
    instance = vote.publication or vote.comment
    if instance.dislikes > 0:
        instance.dislikes -= 1
        instance.save()
    if instance.created_by.profile.dislikes > 0:
        instance.created_by.profile.dislikes -= 1
        instance.created_by.profile.save()
    if hasattr(instance, "community") and instance.community and instance.community.dislikes > 0:
        instance.community.dislikes -= 1
        instance.community.save()


def decrease_supports(vote):
    instance = vote.publication or vote.comment
    if instance.supports > 0:
        instance.supports -= 1
        instance.save()
    if instance.created_by.profile.supports > 0:
        instance.created_by.profile.supports -= 1
        instance.created_by.profile.save()
    if hasattr(instance, "community") and instance.community and instance.community.supports > 0:
        instance.community.supports -= 1
        instance.community.save()


def notify_author(fieldset, send_to):
    notification = Notification.objects.create(**fieldset)
    NotificationTo.objects.create(notification=notification, user=send_to)
