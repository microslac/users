from django.db import models
from micro.jango.models import HistoryModel, UUIDModel

from users.models import User


class UserAvatar(HistoryModel, UUIDModel):
    id = models.AutoField(primary_key=True)
    team_id = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="avatar")
    avatar_hash = models.CharField(max_length=255, default="")
    temp_hash = models.CharField(max_length=255, default="")
    metadata = models.JSONField(default=dict, null=True)

    class Meta:
        db_table = "user_avatars"
        ordering = ["-created"]
