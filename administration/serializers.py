from rest_framework import serializers

from administration.models import Administration, PageView


class AdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administration
        exclude = ["id"]


class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        exclude = ["id"]
