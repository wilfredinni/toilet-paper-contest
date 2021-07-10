from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.AccountRegistrationAPIView.as_view()),
    path("activate/<int:id>/", views.AccountActivationAPIView.as_view()),
]
