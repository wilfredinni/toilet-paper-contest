from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.email

    @staticmethod
    def activate_account(user_instance, validated_data):
        new_password = validated_data.get("password")
        user_instance.set_password(new_password)
        user_instance.is_active = True
        user_instance.save()

        return user_instance
