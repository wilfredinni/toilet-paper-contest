from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer, UserActivationSerializer
from apps.users.models import CustomUser


class AccountRegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class AccountActivationAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserActivationSerializer
    lookup_field = "id"
