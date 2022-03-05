from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from administration.models import Administration


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
