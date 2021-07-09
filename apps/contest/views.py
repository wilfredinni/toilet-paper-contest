import random

from rest_framework import viewsets
from django.db.models import Max

from ..users.models import CustomUser
from .serializers import UserSerializer


class ContestWinnerViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        # exclude staff and non active users
        queryset = CustomUser.objects.filter(
            is_active=True, is_superuser=False, is_staff=False
        )

        # more performant than .order_by("?")[:1]
        return [random.choice(queryset)]
