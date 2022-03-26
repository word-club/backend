from comment.models import Comment


def _get_target(trigger, search_for=None):
    target = None
    if not search_for:
        search_for = ["publication", "comment", "community", "profile"]
    for key in search_for:
        if hasattr(trigger, key) and getattr(trigger, key):
            target = getattr(trigger, key)
            break
    return target


def add_popularity(trigger):
    target = _get_target(trigger)
    target.popularity += 1
    target.save()


def add_supports(trigger):
    target = _get_target(trigger)
    target.supports += 1
    target.save()


def add_dislikes(trigger):
    target = _get_target(trigger)
    target.dislikes += 1
    target.save()


def decrease_popularity(trigger):
    target = _get_target(trigger)
    if target.popularity > 0:
        target.popularity -= 1
        target.save()


def decrease_dislikes(trigger):
    target = _get_target(trigger)
    if target.dislikes > 0:
        target.dislikes -= 1
        target.save()


def decrease_supports(trigger):
    target = _get_target(trigger)
    if target.supports > 0:
        target.supports -= 1
        target.save()


def add_discussions(trigger: Comment):
    publication = trigger.publication
    publication.discussions += 1
    publication.save()
    trigger.created_by.profile.discussions += 1
    trigger.created_by.profile.save()
    if trigger.reply:
        trigger.reply.discussions += 1
        trigger.reply.save()
    community = trigger.publication.community
    if community:
        community.discussions += 1
        community.save()


def decrease_discussions(trigger: Comment):
    publication = trigger.publication
    if publication.discussions > 0:
        publication.discussions -= 1
        publication.save()
    if trigger.created_by.profile.discussions > 0:
        trigger.created_by.profile.discussions -= 1
        trigger.created_by.profile.save()
    if trigger.reply and trigger.reply.discussions > 0:
        trigger.reply.discussions -= 1
        trigger.reply.save()
    community = trigger.publication.community
    if community and community.discussions > 0:
        community.discussions -= 1
        community.save()
