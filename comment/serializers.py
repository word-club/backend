from comment.helper import *
from globals import UserGlobalSerializer, PublicationForUserCommentSerializer


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


class ReplySerializer(serializers.ModelSerializer):
    # reactions = serializers.SerializerMethodField()
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    share_status = serializers.SerializerMethodField()
    hidden_status = serializers.SerializerMethodField()
    bookmark_status = serializers.SerializerMethodField()

    # @staticmethod
    # def get_reactions(obj):
    #     return get_comment_reactions(obj)

    def get_up_vote(self, obj):
        user = self.context["user"]
        return get_my_upvote(user, obj)

    def get_down_vote(self, obj):
        user = self.context["user"]
        return get_my_downvote(user, obj)

    def get_share_status(self, obj):
        user = self.context["user"]
        return get_my_share_status(user, obj)

    def get_hidden_status(self, obj):
        user = self.context["user"]
        return get_my_hidden_status(user, obj)

    def get_bookmark_status(self, obj):
        user = self.context["user"]
        return get_my_bookmark_status(user, obj)

    class Meta:
        model = Comment
        exclude = ["reply"]


class CommentForProfileSerializer(serializers.ModelSerializer):
    publication = PublicationForUserCommentSerializer()
    reactions = serializers.SerializerMethodField()
    images = CommentImageSerializer(many=True, read_only=True)
    image_urls = CommentImageUrlSerializer(many=True, read_only=True)

    @staticmethod
    def get_reactions(obj):
        return get_comment_reactions(obj)

    class Meta:
        model = Comment
        exclude = ["created_by"]


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
            replies, many=True, context={"user": self.context["user"]}
        ).data

    @staticmethod
    def get_reactions(obj):
        return get_comment_reactions(obj)

    def get_up_vote(self, obj):
        user = self.context["user"]
        return get_my_upvote(user, obj)

    def get_down_vote(self, obj):
        user = self.context["user"]
        return get_my_downvote(user, obj)

    def get_share_status(self, obj):
        user = self.context["user"]
        return get_my_share_status(user, obj)

    def get_hidden_status(self, obj):
        user = self.context["user"]
        return get_my_hidden_status(user, obj)

    def get_bookmark_status(self, obj):
        user = self.context["user"]
        return get_my_bookmark_status(user, obj)

    class Meta:
        model = Comment
        fields = "__all__"
