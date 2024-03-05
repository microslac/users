from micro.jango.tests.base import UnitTestBase

from users.models import User


class TestUserModel(UnitTestBase):
    def test_create_user(self):
        auth_id = "A0123546789"
        team_id = "T0123546789"
        user = User.objects.create(auth_id=auth_id, team_id=team_id, name="user")

        assert user.id.startswith("U")
        assert user.uuid
        assert user.name == "user"
        assert user.auth_id == auth_id
        assert user.team_id == team_id
        assert user.created is not None
