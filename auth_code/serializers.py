from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(new_password):
        validate_password(new_password)
        return new_password

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "New password must match with confirm password."
            )
        return data
