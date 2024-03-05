from django.db import models
from micro.jango.models import DeletedModel, HistoryModel, UUIDModel
from micro.jango.models.fields import ShortIdField


class User(UUIDModel, DeletedModel, HistoryModel):
    id = ShortIdField(prefix="U", primary_key=True)
    name = models.CharField(max_length=255, blank=True, default="")
    auth_id = models.CharField(max_length=50, blank=False, null=False)
    team_id = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = "users"
        unique_together = ("auth_id", "team_id")
        ordering = ["-created"]
