import jwt

from rest_framework import serializers

from django.conf import settings

from .tasks import send_activation_email
from ..users.models import CustomUser


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
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def update(self, instance, validated_data):
        try:
            # get and validate the token
            token = self.context["request"].query_params.get("token")
            jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            # set the user password and activate the account
            new_password = validated_data.get("password")
            instance.set_password(new_password)
            instance.is_active = True
            instance.save()

            return instance

        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            raise serializers.ValidationError({"token": "Token is missing or invalid."})
