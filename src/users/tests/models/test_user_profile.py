from micro.jango.tests.base import UnitTestBase

from tests.factories import UserFactory
from users.models import UserProfile


class TestUserProfileModel(UnitTestBase):
    def test_create_user(self):
        user = UserFactory()
        email = "user@example.com"
        profile = UserProfile.objects.create(user=user, real_name=user.name, email=email)

        assert profile.user.id == user.id
        assert user.profile.id == profile.id
        assert profile.created is not None

        assert profile.email == email
        assert profile.display_name == ""
        assert profile.real_name == user.name
        assert profile.first_name == profile.display_name.split(" ").pop(0)
        assert profile.last_name == profile.display_name.split(" ").pop()

        assert profile.phone == ""
        assert profile.skype == ""
        assert profile.title == ""
        assert profile.avatar_hash == ""
