# vote signal helper functions

def add_popularity(vote):
    instance = vote.publication if vote.publication else vote.comment
    instance.popularity += 1
    instance.save()
    instance.created_by.profile.popularity += 1
    instance.created_by.profile.save()
    if instance.community:
        instance.community.popularity += 1
        instance.community.save()


def add_supports(vote):
    instance = vote.publication if vote.publication else vote.comment
    instance.supports += 1
    instance.save()
    instance.created_by.profile.supports += 1
    instance.created_by.profile.save()
    if instance.community:
        instance.community.supports += 1
        instance.community.save()


def add_dislikes(vote):
    instance = vote.publication if vote.publication else vote.comment
    instance.dislikes += 1
    instance.save()
    instance.created_by.profile.dislikes += 1
    instance.created_by.profile.save()
    if instance.community:
        instance.community.dislikes += 1
        instance.community.save()


def decrease_popularity(vote):
    instance = vote.publication if vote.publication else vote.comment
    if instance.popularity > 0:
        instance.popularity -= 1
        instance.save()
    if instance.created_by.profile.popularity > 0:
        instance.created_by.profile.popularity -= 1
        instance.created_by.profile.save()
    if instance.community and instance.community.popularity > 0:
        instance.community.popularity -= 1
        instance.community.save()


def decrease_dislikes(vote):
    instance = vote.publication if vote.publication else vote.comment
    if instance.dislikes > 0:
        instance.dislikes -= 1
        instance.save()
    if instance.created_by.profile.dislikes > 0:
        instance.created_by.profile.dislikes -= 1
        instance.created_by.profile.save()
    if instance.community and instance.community.dislikes > 0:
        instance.community.dislikes -= 1
        instance.community.save()


def decrease_supports(vote):
    instance = vote.publication if vote.publication else vote.comment
    if instance.supports > 0:
        instance.supports -= 1
        instance.save()
    if instance.created_by.profile.supports > 0:
        instance.created_by.profile.supports -= 1
        instance.created_by.profile.save()
    if instance.community and instance.community.supports > 0:
        instance.community.supports -= 1
        instance.community.save()


def notify_author(instance, created):
    # TODO
    pass
