from tests.factories import UserFactory
from tests.internal import InternalTestBase


class TestLookupUser(InternalTestBase):
    def test_lookup_user_failed(self):
        user = UserFactory()
        data = dict(team=user.team_id, user=reversed(user.id))  # failed
        self.client_request(f"{self.URL}/lookup", data=data, internal=True, status=400, ok=False)

    def test_lookup_user_success(self):
        user = UserFactory()
        data = dict(team=user.team_id, user=user.id)
        resp = self.client_request(f"{self.URL}/lookup", data=data, internal=True, status=200, ok=True)
        assert resp.user.id == user.id

    def test_lookup_user_by_auth_and_team_success(self):
        user = UserFactory()
        data = dict(auth=user.auth_id, team=user.team_id)
        resp = self.client_request(f"{self.URL}/lookup", data=data, internal=True, status=200, ok=True)
        assert resp.user.id == user.id
