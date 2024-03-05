import re

from django.db import models
from micro.jango.models import HistoryModel, ShortIdField, UUIDModel

from users.managers import UserProfileManager
from users.models import User


class UserProfile(HistoryModel, UUIDModel):
    id = ShortIdField(prefix="P", primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.CharField(max_length=255, null=False, blank=False)
    real_name = models.CharField(max_length=255, blank=False)
    display_name = models.CharField(max_length=225, default="")
    phone = models.CharField(max_length=50, default="")
    skype = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")

    avatar_hash = models.CharField(max_length=255, default="")

    objects = UserProfileManager()

    @property
    def first_name(self) -> str:
        display_name = str(self.display_name)
        return re.split(r"\s+", display_name).pop(0)

    @property
    def last_name(self) -> str:
        display_name = str(self.display_name)
        return re.split(r"\s+", display_name).pop()

    class Meta:
        db_table = "user_profiles"
        ordering = ["-created"]
