def add_popularity(instance, created):
    if created:
        publication = instance.publication
        if publication.popularity > 0:
            publication.popularity += 1
            publication.save()
        if publication.created_by.profile.popularity > 0:
            publication.created_by.profile.popularity += 1
            publication.created_by.profile.save()
        if publication.community and publication.community.popularity > 0:
            publication.community.popularity += 1
            publication.community.save()


def add_dislikes(instance, created):
    if created:
        publication = instance.publication
        if publication.dislikes > 0:
            publication.dislikes += 1
            publication.save()
        if publication.created_by.profile.dislikes > 0:
            publication.created_by.profile.dislikes += 1
            publication.created_by.profile.save()
        if publication.community and publication.community.dislikes > 0:
            publication.community.dislikes += 1
            publication.community.save()


def add_supports(instance, created):
    if created:
        publication = instance.publication
        if publication.supports > 0:
            publication.supports += 1
            publication.save()
        if publication.created_by.profile.supports > 0:
            publication.created_by.profile.supports += 1
            publication.created_by.profile.save()
        if publication.community and publication.community.supports > 0:
            publication.community.supports += 1
            publication.community.save()


def decrease_popularity(instance):
    publication = instance.publication
    if publication.popularity > 0:
        publication.popularity -= 1
        publication.save()
    if publication.created_by.profile.popularity > 0:
        publication.created_by.profile.popularity -= 1
        publication.created_by.profile.save()
    if publication.community and publication.community.popularity > 0:
        publication.community.popularity -= 1
        publication.community.save()


def decrease_dislikes(instance):
    publication = instance.publication
    if publication.dislikes > 0:
        publication.dislikes -= 1
        publication.save()
    if publication.created_by.profile.dislikes > 0:
        publication.created_by.profile.dislikes -= 1
        publication.created_by.profile.save()
    if publication.community and publication.community.dislikes > 0:
        publication.community.dislikes -= 1
        publication.community.save()


def decrease_supports(instance):
    publication = instance.publication
    if publication.supports > 0:
        publication.supports -= 1
        publication.save()
    if publication.created_by.profile.supports > 0:
        publication.created_by.profile.supports -= 1
        publication.created_by.profile.save()
    if publication.community and publication.community.supports > 0:
        publication.community.supports -= 1
        publication.community.save()


def notify_author(instance, created):
    # TODO
    pass
