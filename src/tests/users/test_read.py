import pytest
from rest_framework import status

from tests.factories import UserFactory, UserProfileFactory
from tests.users import UsersTestBase


class TestReadUser(UsersTestBase):
    @pytest.mark.parametrize("include_profile", (True,))
    def test_get_user_success(self, client, include_profile):
        user = UserFactory()
        profile = UserProfileFactory(user=user)
        data = dict(team=user.team_id, user=user.id, include_profile=include_profile)
        resp = self.client_request(f"{self.URL}/info", data=data, status=status.HTTP_200_OK, ok=True)

        assert resp.user.id == user.id
        assert resp.user.team == user.team_id
        assert resp.user.name == user.name
        assert resp.user.created
        assert resp.user.updated

        assert resp.user.profile.email == profile.email
        assert resp.user.profile.real_name == profile.real_name
