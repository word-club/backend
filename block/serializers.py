from rest_framework import serializers

from block.models import Block


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = "__all__"


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        exclude = ['community']


class BlockCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        exclude = ['user']
