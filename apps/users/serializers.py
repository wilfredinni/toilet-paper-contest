from rest_framework import serializers

from ..users.models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "bio",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        new_user = CustomUser.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            phone=validated_data.get("phone"),
            address=validated_data.get("address"),
            bio=validated_data.get("bio"),
        )

        new_user.is_active = False
        new_user.save()

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
        password = validated_data.get("password")
        instance.set_password(password)
        instance.is_active = True
        instance.save()
        return instance
