import json

from django.conf import settings

from clients.kafka import produce_message


def generate_profile_message(profile):
    username = profile.user.username
    profile_dict = {'user.username': username, 'profile.uuid': str(profile.uuid), 'profile.role': profile.role.name}
    profile_message = json.dumps(profile_dict)
    return profile_message


def send_profile_role_changed(profile):
    message = generate_profile_message(profile=profile)
    produce_message(topic=settings.KAFKA_TOPIC_PROFILES_ROLE_CHANGED, message=message)
