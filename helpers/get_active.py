from collections import OrderedDict
from pprint import pprint

from avatar.models import Avatar
from cover.models import Cover


def get_active_item_for(model_class, filterset=None, request=None):
    if filterset is None or not isinstance(filterset, dict):
        filterset = OrderedDict()

    filterset["is_active"] = True
    try:
        item = model_class.objects.get(**filterset)
        if request is None:
            return item.image.url

        return "{}://{}{}".format(
            getattr(request, "_request").scope.get("scheme"),
            request.META.get("HTTP_HOST"), item.image.url
        )
    except model_class.DoesNotExist:
        return None


def get_active_avatar_for(filterset=None, request=None):
    return get_active_item_for(Avatar, filterset, request)


def get_active_cover_for(filterset=None, request=None):
    return get_active_item_for(Cover, filterset, request)
