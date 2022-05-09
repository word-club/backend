import collections
from notification.models import Notification, NotificationTo


def prepare_fieldset(target, instance, verb=None, description=None, subject=None):
    fieldset = collections.OrderedDict()
    fieldset[instance.__class__.__name__.lower()] = instance
    fieldset["subject"] = subject or instance.__class__.__name__.capitalize()
    if description:
        fieldset["description"] = description
    else:
        creator = instance.created_by
        fieldset["description"] = (
            f'User "{creator.profile.display_name or creator.username}" has '
            f"{verb}"
            f" your {target.__class__.__name__.lower()}"
            f' "{target.__str__()}".'
        )
    return fieldset


def notify_author(target, instance, verb=None, description=None, subject=None):
    fieldset = prepare_fieldset(target, instance, verb, description, subject)
    notification = Notification.objects.create(**fieldset)
    NotificationTo.objects.create(notification=notification, user=target.created_by)
