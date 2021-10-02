from rest_framework import serializers
from notification.models import *
from publication.models import Publication


class NotificationPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationNotification
        fields = "__all__"


class NotificationCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityNotification
        fields = "__all__"


class NotificationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentNotification
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    publications = NotificationPublicationSerializer(many=True, read_only=True)
    communities = NotificationCommunitySerializer(many=True, read_only=True)
    comments = NotificationCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"


class NotificationReceiverSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = NotificationTo
        fields = "__all__"


class NotificationPostSerializer(serializers.ModelSerializer):
    to_list = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all()),
        max_length=1000,
        required=False
    )
    publication = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Publication.objects.all()),
        max_length=1000,
        required=False
    )
    community = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Community.objects.all()),
        max_length=1000,
        required=False
    )
    comment = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all()),
        max_length=1000,
        required=False
    )

    class Meta:
        model = Notification
        fields = "__all__"

    def create(self, validated_data):
        to_list = validated_data.get("to_list")
        publications = validated_data.get("publication")
        communities = validated_data.get("community")
        comments = validated_data.get("comment")

        is_global = True if validated_data.get("is_global") is True else False

        notification = Notification.objects.create(
            subject=validated_data.get("subject"),
            description=validated_data.get("description"),
            is_global=is_global,
        )

        if to_list: [
            NotificationTo.objects.create(
                notification=notification,
                user=user
            ) for user in to_list
        ]
        if publications: [
            PublicationNotification.objects.create(
                notification=notification,
                publication=publication
            ) for publication in publications
        ]
        if communities: [
            CommunityNotification.objects.create(
                notification=notification,
                community=community
            ) for community in communities
        ]
        if comments: [
            CommentNotification.objects.create(
                notification=notification,
                comment=comment
            ) for comment in comments
        ]
        return notification
