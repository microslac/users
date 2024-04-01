from micro.jango.serializers import BaseModelSerializer, BaseSerializer, TimestampField
from rest_framework import serializers

from users.models import User, UserProfile


class UserProfileSerializer(BaseModelSerializer):
    id = serializers.CharField(required=False, write_only=True)
    user = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "email",
            "real_name",
            "display_name",
            "first_name",
            "last_name",
            "phone",
            "skype",
            "title",
            "avatar_hash",
        )
        write_only_fields = ("id", "user")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = {k: v for k, v in data.items() if v is not None}
        return data


class UserSerializer(BaseModelSerializer):
    auth = serializers.CharField(required=True, write_only=True)
    team = serializers.CharField(required=True, write_only=True)
    created = TimestampField(required=False, read_only=True)
    updated = TimestampField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "auth", "team", "created", "updated")

    def to_representation(self, instance: User):
        data = super().to_representation(instance)
        data.update(team=instance.team_id)
        if self.context.get("include_profile", True):
            data.update(profile=UserProfileSerializer(instance.profile).data)
        return data


class UserCreateSerializer(BaseSerializer):
    auth = serializers.CharField(required=True, allow_blank=False)
    team = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    name = serializers.CharField(required=False, allow_blank=True, default="")


class UserLookupSerializer(BaseSerializer):
    auth = serializers.CharField(required=False, allow_blank=False)
    team = serializers.CharField(required=False, allow_blank=False)
    user = serializers.CharField(required=False, allow_blank=False)


class UserCrudSerializer(BaseSerializer):
    team = serializers.CharField(required=True, write_only=True)
    user = serializers.CharField(required=True, allow_blank=False)


class UserInfoSerializer(UserCrudSerializer):
    include_profile = serializers.BooleanField(required=False, default=True)


class PrepareAvatarSerializer(UserCrudSerializer):
    image = serializers.FileField(allow_empty_file=False)


class SetAvatarSerializer(UserCrudSerializer):
    image = serializers.IntegerField(required=True)


class RemoveAvatarSerializer(UserCrudSerializer):
    pass


class SetProfileSerializer(UserCrudSerializer):
    real_name = serializers.CharField(required=False, allow_blank=True, default=None)
    display_name = serializers.CharField(required=False, allow_blank=True, default=None)
    title = serializers.CharField(required=False, allow_blank=True, default=None)
    skype = serializers.CharField(required=False, allow_blank=True, default=None)
    phone = serializers.CharField(required=False, allow_blank=True, default=None)
