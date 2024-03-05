import pytest

from tests.internal import InternalTestBase
from users.models import UserProfile


class TestCreateUser(InternalTestBase):
    @pytest.mark.parametrize("missing", ("auth", "team"))
    def test_create_user_invalid(self, missing):
        data = dict(auth="A0123456789", team="T0123456789")
        data.pop(missing)
        resp = self.client_request(f"{self.URL}/create", data=data, internal=True, status=400, ok=False)
        assert resp.error == "required"

    @pytest.mark.parametrize("include_profile", (True, False))
    def test_create_user_success(self, include_profile):
        auth_id, team_id, email = "A0123456789", "T0123456789", "user@example.com"
        data = dict(auth=auth_id, team=team_id, email=email, include_profile=include_profile)
        resp = self.client_request(f"{self.URL}/create", data=data, internal=True, status=200, ok=True)

        assert getattr(resp.user, "auth", None) is None
        assert resp.user.id.startswith("U")
        assert resp.user.team == team_id
        assert resp.user.created
        assert resp.user.updated

        if include_profile:
            profile = UserProfile.objects.get(user_id=resp.user.id)
            assert resp.user.profile.email == profile.email
            assert resp.user.profile.real_name == profile.real_name
