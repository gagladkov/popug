import json

from django.conf import settings
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from kafka import KafkaConsumer

from clients.kafka_client.json_schema_loader import get_json_schema
from task.logic import update_or_create_profile


def consume_profiles_role_changed():
    consumer = KafkaConsumer(settings.KAFKA_TOPIC_PROFILES_ROLE_CHANGED, bootstrap_servers=[settings.KAFKA_SERVER])
    for message in consumer:
        try:
            validate(instance=message, schema=get_json_schema(topic_name=settings.KAFKA_TOPIC_PROFILES_ROLE_CHANGED))
        except ValidationError:
            print("ochen ploho")
            # save_message_to_some_bd_to_fix_it_later(message)
        profile_data = json.loads(message.value.decode('utf-8'))
        print(profile_data)
        update_or_create_profile(profile_data)
