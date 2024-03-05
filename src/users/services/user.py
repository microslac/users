from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import Q
from micro.jango.services import BaseService

from users.models import User, UserAvatar, UserProfile


class UserService(BaseService):
    @classmethod
    def create_user(cls, auth_id: str, team_id: str, email: str, data: dict, **kwargs) -> User:
        name = data.get("name", "")
        name = name or email.split("@", 1).pop(0)
        user = User.objects.create(auth_id=auth_id, team_id=team_id, name=name)
        user.profile = UserProfile.objects.create(user=user, email=email, real_name=name)
        return user

    @classmethod
    def get_user(cls, team_id: str, user_id: str) -> User:
        user = User.objects.get(team_id=team_id, id=user_id)
        return user

    @classmethod
    def destroy_user(cls, user_id: str):
        user = User.objects.get(id=user_id)
        user.destroy()

    @classmethod
    def lookup_user(cls, user_id: str = None, **kwargs) -> dict | None:
        assert user_id or kwargs

        query = Q(id=user_id) if user_id else Q(**kwargs)
        return User.objects.filter(query).values("id").first()

    @classmethod
    def prepare_avatar(
        cls, team_id: str, user_id: str, image: InMemoryUploadedFile, return_temp: bool = False, **kwargs
    ):
        import hashlib
        from datetime import datetime

        import boto3

        region = settings.AWS_REGION_NAME
        bucket = settings.AWS_BUCKET_NAME
        s3_url = f"https://{bucket}.s3.{region}.amazonaws.com"
        client = boto3.client("s3", region_name=region)

        user = cls.get_user(team_id, user_id)
        now_ts = datetime.utcnow().timestamp()
        seed = ":".join([team_id, user_id, str(now_ts)])
        temp_hash = hashlib.shake_128(seed.encode()).hexdigest(6)

        metadata = dict(
            name=image.name,
            size=image.size,
            content_type=image.content_type,
            extension=image.name.rsplit(".").pop(),
            ts=now_ts,
        )

        with transaction.atomic():
            avatar = UserAvatar.objects.create(
                user_id=user_id,
                team_id=user.team_id,
                temp_hash=temp_hash,
                metadata=metadata,
            )
            image_date = avatar.created.strftime("%Y-%m-%d")
            image_name = f"{avatar.team_id}-{avatar.user_id}-{avatar.temp_hash}"
            temp_key = f"avatars/temp/{image_date}/{image_name}"

            client.put_object(
                Bucket=bucket,
                Key=temp_key,
                Body=image,
                ContentType=image.content_type,
            )

        if return_temp:
            return temp_hash, temp_key
        return dict(id=avatar.id, url=f"{s3_url}/{temp_key}")

    @classmethod
    def set_avatar(cls, team_id: str, user_id: str, image_id: str):
        import hashlib
        from datetime import datetime
        from io import BytesIO

        import boto3
        from PIL import Image

        user = User.objects.get(id=user_id, team_id=team_id)
        avatar: UserAvatar = UserAvatar.objects.filter(id=image_id, user=user).first()

        now_ts = datetime.utcnow().timestamp()
        seed = ":".join([team_id, user_id, str(now_ts)])
        avatar_hash = hashlib.shake_128(seed.encode()).hexdigest(6)

        region = settings.AWS_REGION_NAME
        bucket = settings.AWS_BUCKET_NAME
        s3_url = f"https://{bucket}.s3.{region}.amazonaws.com"
        client = boto3.client("s3", region_name=region)

        image_date = avatar.created.strftime("%Y-%m-%d")
        image_name = f"{avatar.team_id}-{avatar.user_id}-{avatar.temp_hash}"
        temp_key = f"avatars/temp/{image_date}/{image_name}"
        response = client.get_object(Bucket=bucket, Key=temp_key)

        resized_urls = []

        with Image.open(BytesIO(response["Body"].read())) as image:
            content_type = avatar.metadata.get("content_type")
            extension = avatar.metadata.get("extension", "").upper()
            extension = {"JPG": "JPEG"}.get(extension, extension)

            def process(size: int | str):
                img = image.resize((size, size)) if isinstance(size, int) else image
                img_io = BytesIO()
                img.save(img_io, format=extension)
                img_key = f"avatars/{avatar.team_id}-{avatar.user_id}-{avatar_hash}_{size}"

                client.put_object(
                    Bucket=bucket,
                    Key=img_key,
                    Body=img_io.getvalue(),
                    ContentType=content_type,
                )
                resized_urls.append((f"image_{size}", f"{s3_url}/{img_key}"))

            sizes = (24, 32, 48, 72, 256, 512, "original")
            for size in sizes:
                process(size)

        avatar.avatar_hash = avatar_hash
        user.profile.avatar_hash = avatar_hash

        avatar.save()
        user.profile.save()

        return dict(avatar_hash=avatar.avatar_hash, **dict(resized_urls))

    @classmethod
    def remove_avatar(cls, team_id: str, user_id: str, **kwargs) -> None:
        user = User.objects.get(id=user_id, team_id=team_id)
        user.profile.avatar_hash = ""
        user.profile.save()

    @classmethod
    def set_profile(cls, team_id: str, user_id: str, data: dict, **kwargs) -> UserProfile:
        updatable_fields = {"real_name", "display_name", "phone", "skype", "title"}
        data = {k: v for k, v in data.items() if k in updatable_fields and v is not None}

        user = User.objects.get(id=user_id, team_id=team_id)
        profile: UserProfile = user.profile

        for key, value in data.items():
            setattr(profile, key, value)
        profile.save(update_fields=data.keys())

        return profile
