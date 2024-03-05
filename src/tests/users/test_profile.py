from tests.factories import UserFactory, UserProfileFactory
from tests.users import UsersTestBase


class TestUserProfile(UsersTestBase):
    def test_set_user_profile_success(self, client):
        user = UserFactory(id="U0123456789")
        profile = UserProfileFactory(user=user)
        data = dict(real_name="Real Name", display_name="Display Name", title="Real Title")
        resp = self.client_request(f"{self.URL}/set-profile", data=data, status=200, ok=True)

        assert resp.profile.title == data["title"]
        assert resp.profile.real_name == data["real_name"]
        assert resp.profile.display_name == data["display_name"]

        profile.refresh_from_db()
        assert resp.profile.title == profile.title
        assert resp.profile.real_name == profile.real_name
        assert resp.profile.display_name == profile.display_name
