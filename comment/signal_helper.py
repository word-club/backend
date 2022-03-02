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
