from django.conf import settings
from django.urls import include
from django.urls import re_path as url
from rest_framework import routers

from users.views import InternalViewSet, UserViewSet

app_name = settings.APP_USERS
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="User")
router.register(r"internal", InternalViewSet, basename="Internal")

urlpatterns = [
    url(r"^", include(router.urls)),
]
