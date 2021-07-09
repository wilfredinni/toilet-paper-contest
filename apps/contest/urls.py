from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"contest-winner", views.ContestWinnerViewset, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
