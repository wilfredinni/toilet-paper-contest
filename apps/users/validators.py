import jwt

from django.conf import settings

from rest_framework import serializers


def password_validator(attrs):
    if attrs["password"] != attrs["password2"]:
        raise serializers.ValidationError({"password": "Password fields didn't match."})


def token_validator(token):
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        raise serializers.ValidationError({"token": "Token is missing or invalid."})
