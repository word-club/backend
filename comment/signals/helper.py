def add_pub_discussions(instance, created):
    if created and instance.publication:
        instance.publication.discussions += 1
        instance.publication.save()
        if instance.reply:
            instance.reply.discussions += 1
            instance.reply.save()


def decrease_pub_discussions(instance):
    if instance.publication:
        instance.publication.discussions -= 1
        instance.publication.save()
        if instance.reply:
            instance.reply.discussions -= 1
            instance.reply.save()


def add_popularity(instance, created):
    if created:
        instance.comment.popularity += 1
        instance.comment.save()
        instance.comment.created_by.profile.popularity += 1
        instance.comment.created_by.profile.save()


def add_dislikes(instance, created):
    if created:
        instance.comment.dislikes += 1
        instance.comment.save()
        instance.comment.created_by.profile.dislikes += 1
        instance.comment.created_by.profile.save()


def add_supports(instance, created):
    if created:
        instance.comment.supports += 1
        instance.comment.save()
        instance.comment.created_by.profile.supports += 1
        instance.comment.created_by.profile.save()


def decrease_popularity(instance):
    instance.comment.popularity -= 1
    instance.comment.save()
    instance.comment.created_by.profile.popularity -= 1
    instance.comment.created_by.profile.save()


def decrease_dislikes(instance):
    instance.comment.dislikes -= 1
    instance.comment.save()

    instance.comment.created_by.profile.dislikes -= 1
    instance.comment.created_by.profile.save()


def decrease_supports(instance):
    instance.comment.supports -= 1
    instance.comment.save()
    instance.comment.created_by.profile.supports -= 1
    instance.comment.created_by.profile.save()
