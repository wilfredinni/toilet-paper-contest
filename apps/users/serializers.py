from rest_framework import serializers

from apps.users.models import CustomUser
from .validators import password_validator, token_validator
from .tasks import send_activation_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "bio",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        validated_data["is_active"] = False
        new_user = CustomUser.objects.create(**validated_data)
        send_activation_email.delay(new_user.id)
        return new_user


class UserActivationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2", "is_active"]
        read_only_fields = ["is_active", "email", "username"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        token = self.context["request"].query_params.get("token")
        password_validator(attrs)
        token_validator(token)
        return attrs

    def update(self, instance, validated_data):
        user_instance = CustomUser.activate_account(instance, validated_data)
        return user_instance
