import json

from django.conf import settings
from kafka import KafkaConsumer

from task.logic import update_or_create_profile


def consume_profiles_role_changed():
    consumer = KafkaConsumer(settings.KAFKA_TOPIC_PROFILES_ROLE_CHANGED, bootstrap_servers=[settings.KAFKA_SERVER])
    for message in consumer:
        profile_data = json.loads(message.value.decode('utf-8'))
        print(profile_data)
        update_or_create_profile(profile_data)
