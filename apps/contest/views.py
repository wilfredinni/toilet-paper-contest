import random

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ..users.models import CustomUser
from .serializers import UserSerializer


class ContestWinnerViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ["get"]

    def get_queryset(self):
        # exclude staff and non active users
        queryset = CustomUser.objects.filter(
            is_active=True, is_superuser=False, is_staff=False
        )

        # more performant than .order_by("?")[:1]
        if queryset:
            return [random.choice(queryset)]

        return queryset
