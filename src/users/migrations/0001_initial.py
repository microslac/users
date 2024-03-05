# Generated by Django 5.0.2 on 2024-03-24 11:52

import uuid

import django.db.models.deletion
import micro.jango.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("deleted", models.DateTimeField(null=True)),
                ("deleter_id", models.CharField(default="", max_length=20)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("creator_id", models.CharField(default="", max_length=20)),
                ("updater_id", models.CharField(default="", max_length=20)),
                (
                    "id",
                    micro.jango.models.fields.ShortIdField(
                        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=11,
                        max_length=20,
                        prefix="U",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, default="", max_length=255)),
                ("auth_id", models.CharField(max_length=50)),
                ("team_id", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "users",
                "ordering": ["-created"],
                "unique_together": {("auth_id", "team_id")},
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("creator_id", models.CharField(default="", max_length=20)),
                ("updater_id", models.CharField(default="", max_length=20)),
                (
                    "id",
                    micro.jango.models.fields.ShortIdField(
                        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=11,
                        max_length=20,
                        prefix="P",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.CharField(max_length=255)),
                ("real_name", models.CharField(max_length=255)),
                ("display_name", models.CharField(default="", max_length=225)),
                ("phone", models.CharField(default="", max_length=50)),
                ("skype", models.CharField(default="", max_length=255)),
                ("title", models.CharField(default="", max_length=255)),
                ("avatar_hash", models.CharField(default="", max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="users.user"
                    ),
                ),
            ],
            options={
                "db_table": "user_profiles",
                "ordering": ["-created"],
            },
        ),
    ]
