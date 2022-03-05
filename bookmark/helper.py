def add_popularity(trigger):
    instance = trigger.comment or trigger.publication or trigger.community
    instance.popularity += 1
    instance.save()
    instance.created_by.profile.popularity += 1
    instance.created_by.profile.save()
    if trigger.publication:
        trigger.publication.popularity += 1
        trigger.publication.save()


def add_supports(trigger):
    instance = trigger.comment or trigger.publication or trigger.community
    instance.supports += 1
    instance.save()
    instance.created_by.profile.supports += 1
    instance.created_by.profile.save()
    if trigger.publication:
        trigger.publication.supports += 1
        trigger.publication.save()


def decrease_popularity(trigger):
    instance = trigger.comment or trigger.publication or trigger.community
    if instance.popularity > 0:
        instance.popularity -= 1
        instance.save()
    if instance.created_by.profile.popularity > 0:
        instance.created_by.profile.popularity -= 1
        instance.created_by.profile.save()
    if trigger.publication:
        if trigger.publication.popularity > 0:
            trigger.publication.popularity -= 1
            trigger.publication.save()


def decrease_supports(trigger):
    instance = trigger.comment or trigger.publication or trigger.community
    if instance.supports > 0:
        instance.supports -= 1
        instance.save()
    if instance.created_by.profile.supports > 0:
        instance.created_by.profile.supports -= 1
        instance.created_by.profile.save()
    if trigger.publication:
        if trigger.publication.supports > 0:
            trigger.publication.supports -= 1
            trigger.publication.save()
