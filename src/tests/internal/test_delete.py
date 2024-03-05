from tests.factories import UserFactory, UserProfileFactory
from tests.internal import InternalTestBase
from users.models import User, UserProfile


class TestDeleteUser(InternalTestBase):
    def test_destroy_team_success(self):
        user = UserFactory()
        UserProfileFactory(user=user)
        data = dict(team=user.team_id, user=user.id)
        self.client_request(f"{self.URL}/destroy", data=data, internal=True, status=200, ok=True)

        users = User.objects.include_deleted()
        profiles = UserProfile.objects.all()
        assert len(users) == 0
        assert len(profiles) == 0
