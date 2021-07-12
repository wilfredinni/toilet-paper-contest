import random
from django.db.models import Max

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ..users.models import CustomUser
from .serializers import UserSerializer


class ContestWinnerViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ["get"]

    def get_queryset(self):
        # seems to be the more performant solution
        # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html
        # ugly but effective !!!
        eligible_users = CustomUser.objects.filter(
            is_active=True, is_staff=False, is_superuser=False
        )
        max_id = eligible_users.aggregate(max_id=Max("id"))["max_id"]
        pk = random.randint(1, max_id)
        user = eligible_users.filter(pk=pk)
        return user
