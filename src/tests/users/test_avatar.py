import boto3
import pytest
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from moto import mock_aws

from tests.base import UnitTestBase
from tests.factories import UserFactory, UserProfileFactory
from tests.users import UsersTestBase
from users.models.user_avatar import UserAvatar
from users.services import UserService


@pytest.fixture
def mock_image():
    def func():
        from io import BytesIO

        from PIL import Image

        img_io = BytesIO()
        img = Image.new("RGB", (1, 1), color=(255, 255, 255))
        img.save(img_io, format="JPEG")
        img_io.seek(0)

        img_memory = InMemoryUploadedFile(
            img_io,
            None,
            "avatar.jpg",
            "image/jpeg",
            size=img_io.getbuffer().nbytes,
            charset=None,
        )
        return img_memory

    return func


class TestUserPhotoUnit(UnitTestBase):
    @mock_aws
    def test_prepare_photo_success(self, mock_image):
        user = UserFactory()
        client = boto3.client("s3")
        client.create_bucket(
            Bucket=settings.AWS_BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": settings.AWS_REGION_NAME},
        )
        temp_hash, temp_key = UserService.prepare_avatar(user.team_id, user.id, image=mock_image(), return_temp=True)

        response = client.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=temp_key)
        assert response["Body"].read() == mock_image().read()

        avatar = UserAvatar.objects.get(team_id=user.team_id, user_id=user.id)
        assert avatar.temp_hash == temp_hash
        assert avatar.avatar_hash == ""

    @mock_aws
    def test_set_profile_success(self):
        pass


class TestUserAvatarApi(UsersTestBase):
    def test_remove_photo_success(self):
        user = UserFactory(id="U0123456789")
        profile = UserProfileFactory(user=user, avatar_hash="hashed")
        self.client_request(f"{self.URL}/remove-photo", status=200, ok=True)

        profile.refresh_from_db()
        assert profile.avatar_hash == ""
