from rest_framework import serializers

from bookmark.models import Bookmark
from bookmark.serializers import BookmarkSerializer
from comment.models import *
from share.models import Share
from vote.models import Vote
from vote.serializers import VoteSerializer


class HideCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HideComment
        exclude = ["comment"]


def get_my_upvote(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        up_vote = Vote.objects.get(
            created_by=user,
            comment=obj,
            up=True
        )
        return VoteSerializer(up_vote).data
    except Vote.DoesNotExist:
        return False


def get_my_downvote(user, obj):
    if type(user) != get_user_model():
        return False
    try:
        down_vote = Vote.objects.get(
            created_by=user,
            comment=obj,
            up=False
        )
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
        instance = HideComment.objects.get(created_by=user, comment=obj)
        return HideCommentSerializer(instance).data
    except HideComment.DoesNotExist:
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
