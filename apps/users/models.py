from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.email
