from collections import OrderedDict

from avatar.models import Avatar
from cover.models import Cover


def get_active_avatar_for(filterset=None):
    if filterset is None and type(filterset) != dict:
        filterset = OrderedDict()
    filterset["is_active"] = True
    try:
        return Avatar.objects.get(**filterset).image.url
    except Avatar.DoesNotExist:
        return None


def get_active_cover_for(filterset=None):
    if filterset is None and type(filterset) != dict:
        filterset = OrderedDict()
    filterset["is_active"] = True
    try:
        return Cover.objects.get(**filterset).image.url
    except Cover.DoesNotExist:
        return None
