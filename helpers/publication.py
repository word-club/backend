import re

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from typing import List

from administration.models import Administration
from image.models import Image


def find_image_urls_from_string(string: str) -> List[str]:
    """
    :param string: string
    :return: list of image urls
    """
    regex = r"\b(https?:\/\/\S+(?:png|jpe?g|gif)\S*)\b"
    return re.findall(regex, string)


def check_publication_update_date_limit(obj):
    """
    :param obj: Publication instance
    :return: void if publication is not published yet
        Response(403) if publication update date limit reached
    """
    now = timezone.now()
    if not obj.published_at:
        return
    diff = now - obj.published_at
    limit = Administration.objects.first()
    if diff.days > limit.publication_update_limit:
        return Response(
            {
                "detail": "Sorry, you cannot update the publication after {} days.".format(
                    limit.publication_update_limit
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )


def get_thumbnail_for(publication):
    """
    :param publication: Publication instance
    :return: url to the thumbnail or None
    """
    # if publication.thumbnail:
    #     return publication.thumbnail.url
    if Image.objects.filter(publication=publication).exists():
        img = Image.objects.filter(publication=publication).first()
        return img.image.url if img.image else img.image_url
    if publication.content:
        urls = find_image_urls_from_string(publication.content)
        if len(urls) > 0:
            return urls[0]
    return None
