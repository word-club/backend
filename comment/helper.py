from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from administration.models import Administration
from bookmark.models import Bookmark
from bookmark.serializers import BookmarkSerializer
from comment.models import *
from hide.models import Hide
from hide.serializers import HideSerializer
from share.models import Share
from vote.models import Vote
from vote.serializers import VoteSerializer


def get_my_upvote(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        up_vote = Vote.objects.get(created_by=user, comment=obj, up=True)
        return VoteSerializer(up_vote).data
    except Vote.DoesNotExist:
        return False


def get_my_downvote(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        down_vote = Vote.objects.get(created_by=user, comment=obj, up=False)
        return VoteSerializer(down_vote).data
    except Vote.DoesNotExist:
        return False


def get_my_share_status(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        share = Share.objects.get(created_by=user, comment=obj)
        return Share(share).data
    except Share.DoesNotExist:
        return False


def get_my_hidden_status(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        instance = Hide.objects.get(created_by=user, comment=obj)
        return HideSerializer(instance).data
    except Hide.DoesNotExist:
        return False


def get_my_bookmark_status(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        bookmark = Bookmark.objects.get(created_by=user, comment=obj)
        return BookmarkSerializer(bookmark).data
    except Bookmark.DoesNotExist:
        return False


def get_comment_reactions(obj):
    up_votes = Vote.objects.filter(comment=obj, up=True).count()
    down_votes = Vote.objects.filter(comment=obj, up=False).count()
    shares = Share.objects.filter(comment=obj).count()
    replies = Comment.objects.filter(reply=obj).count()

    return {
        "up_votes": up_votes,
        "down_votes": down_votes,
        "shares": shares,
        "replies": replies,
        "total": up_votes + down_votes + shares + replies,
    }


def check_comment_update_date_limit(obj):
    """
    :param obj: Comment instance
    :return: void if comment date limit is not reached
        Response(403) if publication update date limit reached
    """
    now = timezone.now()
    diff = now - obj.created_at
    limit = Administration.objects.first()
    if diff.days > limit.comment_update_limit:
        return Response(
            {
                "detail": [
                    "Sorry, you cannot update the comment after {} days.".format(
                        limit.comment_update_limit
                    )
                ]
            },
            status=status.HTTP_403_FORBIDDEN,
        )
