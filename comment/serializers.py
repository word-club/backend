from rest_framework import serializers

from comment.models import *
from globals import UserGlobalSerializer


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        return super().create(validated_data)


class CommentImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImageUrl
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        return super().create(validated_data)


class CommentUpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUpVote
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentDownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentDownVote
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class ReplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        comment = self.context["comment"]
        validated_data["reply"] = comment
        validated_data["publication"] = comment.publication
        validated_data["created_by"] = self.context["user"]
        return super().create(validated_data)



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


class ReplySerializer(serializers.ModelSerializer):
    reactions = serializers.SerializerMethodField()
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    share_status = serializers.SerializerMethodField()
    hidden_status = serializers.SerializerMethodField()
    bookmark_status = serializers.SerializerMethodField()

    @staticmethod
    def get_reactions(obj):
        up_votes = CommentUpVote.objects.filter(comment=obj).count()
        down_votes = CommentDownVote.objects.filter(comment=obj).count()
        shares = CommentShare.objects.filter(comment=obj).count()
        replies = Comment.objects.filter(reply=obj).count()

        return up_votes + down_votes + shares + replies

    def get_up_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            up_vote = CommentUpVote.objects.get(created_by=user, comment=obj)
            return CommentUpVoteSerializer(up_vote).data
        except CommentUpVote.DoesNotExist:
            return False

    def get_down_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            down_vote = CommentDownVote.objects.get(created_by=user, comment=obj)
            return CommentDownVoteSerializer(down_vote).data
        except CommentDownVote.DoesNotExist:
            return False

    def get_share_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            share = CommentShare.objects.get(created_by=user, comment=obj)
            return CommentShareSerializer(share).data
        except CommentShare.DoesNotExist:
            return False

    def get_hidden_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            instance = HideComment.objects.get(created_by=user, comment=obj)
            return HideCommentSerializer(instance).data
        except HideComment.DoesNotExist:
            return False

    def get_bookmark_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            bookmark = CommentBookmark.objects.get(created_by=user, comment=obj)
            return CommentBookmarkSerializer(bookmark).data
        except CommentBookmark.DoesNotExist:
            return False

    class Meta:
        model = Comment
        exclude = ["reply"]
        depth = 2


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    images = CommentImageSerializer(many=True, read_only=True)
    image_urls = CommentImageUrlSerializer(many=True, read_only=True)
    created_by = UserGlobalSerializer(read_only=True)

    reactions = serializers.SerializerMethodField()
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    share_status = serializers.SerializerMethodField()
    hidden_status = serializers.SerializerMethodField()
    bookmark_status = serializers.SerializerMethodField()


    def get_replies(self, obj):
        replies = Comment.objects.filter(reply=obj)
        return ReplySerializer(
            replies, many=True,
            context={"user": self.context["user"]}
        ).data


    @staticmethod
    def get_reactions(obj):
        up_votes = CommentUpVote.objects.filter(comment=obj).count()
        down_votes = CommentDownVote.objects.filter(comment=obj).count()
        shares = CommentShare.objects.filter(comment=obj).count()
        comments = Comment.objects.filter(reply=obj).count()

        return up_votes + down_votes + shares + comments

    def get_up_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            up_vote = CommentUpVote.objects.get(created_by=user, comment=obj)
            return CommentUpVoteSerializer(up_vote).data
        except CommentUpVote.DoesNotExist:
            return False

    def get_down_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            down_vote = CommentDownVote.objects.get(created_by=user, comment=obj)
            return CommentDownVoteSerializer(down_vote).data
        except CommentDownVote.DoesNotExist:
            return False

    def get_share_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            share = CommentShare.objects.get(created_by=user, comment=obj)
            return CommentShareSerializer(share).data
        except CommentShare.DoesNotExist:
            return False

    def get_hidden_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            instance = HideComment.objects.get(created_by=user, comment=obj)
            return HideCommentSerializer(instance).data
        except HideComment.DoesNotExist:
            return False

    def get_bookmark_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            bookmark = CommentBookmark.objects.get(created_by=user, comment=obj)
            return CommentBookmarkSerializer(bookmark).data
        except CommentBookmark.DoesNotExist:
            return False


    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2

