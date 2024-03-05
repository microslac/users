from django.db.models.signals import post_save
from django.dispatch import receiver
from micro.events.publishers.registry import communication

from users.models import UserProfile
from users.serializers import UserSerializer


@receiver(post_save, sender=UserProfile, dispatch_uid="user_profile_changed")
def user_profile_changed(sender, instance: UserProfile, **kwargs):
    payload = UserSerializer(instance.user).data
    communication.publish(payload, routing_key="user.profile.changed")
