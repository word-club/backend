from rest_framework import serializers

from comment.models import *
from vote.models import Vote
from vote.serializers import VoteSerializer


class CommentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentShare
        exclude = ["comment"]


class HideCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HideComment
        exclude = ["comment"]


class CommentBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentBookmark
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
        share = CommentShare.objects.get(created_by=user, comment=obj)
        return CommentShareSerializer(share).data
    except CommentShare.DoesNotExist:
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
        bookmark = CommentBookmark.objects.get(created_by=user, comment=obj)
        return CommentBookmarkSerializer(bookmark).data
    except CommentBookmark.DoesNotExist:
        return False


def get_comment_reactions(obj):
    up_votes = CommentUpVote.objects.filter(comment=obj).count()
    down_votes = CommentDownVote.objects.filter(comment=obj).count()
    shares = CommentShare.objects.filter(comment=obj).count()
    replies = Comment.objects.filter(reply=obj).count()

    return {
        "up_votes": up_votes,
        "down_votes": down_votes,
        "shares": shares,
        "replies": replies,
        "total": up_votes + down_votes + shares + replies,
    }
