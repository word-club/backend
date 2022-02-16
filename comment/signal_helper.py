def add_pub_discussions(instance, created):
    if created and instance.publication:
        instance.publication.discussions += 1
        instance.publication.save()
        if instance.reply:
            instance.reply.discussions += 1
            instance.reply.save()


def decrease_pub_discussions(instance):
    if instance.publication:
        if instance.publication.discussions > 0:
            instance.publication.discussions -= 1
            instance.publication.save()
        if instance.reply and instance.reply.discussions > 0:
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
    if instance.comment.popularity > 0:
        instance.comment.popularity -= 1
        instance.comment.save()
    if instance.comment.created_by.profile.popularity > 0:
        instance.comment.created_by.profile.popularity -= 1
        instance.comment.created_by.profile.save()


def decrease_dislikes(instance):
    if instance.comment.dislikes > 0:
        instance.comment.dislikes -= 1
        instance.comment.save()
    if instance.comment.created_by.profile.dislikes > 0:
        instance.comment.created_by.profile.dislikes -= 1
        instance.comment.created_by.profile.save()


def decrease_supports(instance):
    if instance.comment.supports > 0:
        instance.comment.supports -= 1
        instance.comment.save()
    if instance.comment.created_by.profile.supports > 0:
        instance.comment.created_by.profile.supports -= 1
        instance.comment.created_by.profile.save()


def notify_post_subscribers(instance, created):
    if created:
        # TODO
        # for other commentators notify as "someone also have commented on the publication"
        # for author notify as "someone has commented on your publication"
        # for community notify as "someone has commented on a publication posted on your community"
        # for bookmakers notify as "someone has commented on a publication that you've bookmarked on"
        pass


def notify_author(instance, created):
    if created:
        # TODO
        # someone has up voted your publication
        # someone has down voted your publication
        # someone has shared your publication (community information)
        # someone has bookmarked your publication
        pass
