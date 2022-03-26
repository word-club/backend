import collections
from notification.models import Notification, NotificationTo


def prepare_fieldset(target, instance, key, verb=None, description=None, subject=None):
    fieldset = collections.OrderedDict()
    fieldset[key] = instance
    fieldset["subject"] = subject or key.capitalize()
    if description:
        fieldset["description"] = description
    else:
        creator = instance.created_by
        fieldset["description"] = (
            f"{creator.profile.display_name or creator.username} has "
            f"{verb}"
            f" your {target.__class__.__name__.lower()}"
            f' "{target.__str__()}".'
        )
    return fieldset


def update_reaction(trigger, key, add=True):
    instance = None
    if hasattr(trigger, "publication") and trigger.publication:
        instance = trigger.publication
    elif hasattr(trigger, "comment") and trigger.comment:
        instance = trigger.comment
    elif hasattr(trigger, "community") and trigger.community:
        instance = trigger.community
    if instance:
        if add:
            setattr(instance, key, getattr(instance, key) + 1)
        else:
            if getattr(instance, key) > 0:
                setattr(instance, key, getattr(instance, key) - 1)
        instance.save()
        # except for community instances update the authors profile
        if not instance.__class__.__name__ == "Community":
            profile_to_update = instance.created_by.profile
            if add:
                setattr(profile_to_update, key, getattr(profile_to_update, key) + 1)
            else:
                if getattr(profile_to_update, key) > 0:
                    setattr(profile_to_update, key, getattr(profile_to_update, key) - 1)
            profile_to_update.save()
        if hasattr(instance, "community") and instance.community:
            community_to_update = instance.community
            if add:
                setattr(community_to_update, key, getattr(community_to_update, key) + 1)
            else:
                if getattr(community_to_update, key) > 0:
                    setattr(community_to_update, key, getattr(community_to_update, key) - 1)
            community_to_update.save()


def add_popularity(trigger):
    update_reaction(trigger, "popularity")


def add_supports(trigger):
    update_reaction(trigger, "supports")


def add_dislikes(trigger):
    update_reaction(trigger, "dislikes", False)


def decrease_popularity(trigger):
    update_reaction(trigger, "popularity", False)


def decrease_dislikes(trigger):
    update_reaction(trigger, "dislikes", False)


def decrease_supports(trigger):
    update_reaction(trigger, "supports", False)


def notify_author(target, instance, key=None, verb=None, description=None, subject=None):
    fieldset = prepare_fieldset(target, instance, key, verb, description, subject)
    notification = Notification.objects.create(**fieldset)
    if target.__class__.__name__ == "Community":
        # notify to all community subscribers on a published post
        if instance.__class__.__name__ == "Publication":
            from community.sub_models.subscription import Subscription

            subscriptions = Subscription.objects.filter(
                community=target, disable_notification=False, is_approved=True, is_banned=False
            )
            # moderators will be included in the subscription list
            for subscription in subscriptions:
                NotificationTo.objects.create(notification=notification, user=subscription)
        else:
            # notify community moderators if the target is a community instance
            from community.sub_models.moderator import Moderator

            moderators = Moderator.objects.filter(community=target, is_accepted=True, role="MOD")
            for mod in moderators:
                NotificationTo.objects.create(notification=notification, user=mod.user)
    else:
        NotificationTo.objects.create(notification=notification, user=target.created_by)
