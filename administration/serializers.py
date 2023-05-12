from rest_framework import serializers

from administration.models import Administration, PageView


def no_negative(v):
    if v and v < 0:
        raise serializers.ValidationError("Negative value is not allowed.")
    return v


class AdministrationSerializer(serializers.ModelSerializer):
    publication_update_limit = serializers.IntegerField(validators=[no_negative])
    popularity_threshold = serializers.IntegerField(validators=[no_negative])
    comment_update_limit = serializers.IntegerField(validators=[no_negative])
    top_count = serializers.IntegerField(validators=[no_negative])

    class Meta:
        model = Administration
        exclude = ["id"]


class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        exclude = ["id"]
