import factory
from factory.django import DjangoModelFactory
from faker import Factory

from users.models import User, UserProfile

__all__ = ["UserFactory", "UserProfileFactory"]

fake = Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    auth_id = "A0123456789"
    team_id = "T0123456789"
    name = factory.LazyAttribute(lambda _: fake.name())


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    real_name = factory.LazyAttribute(lambda o: o.user.name)
    email = factory.LazyAttribute(fake.email)
