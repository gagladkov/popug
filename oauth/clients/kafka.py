from django.conf import settings
from kafka import KafkaProducer
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from clients.json_schema_loader import get_user_role_changed_json_schema

KAFKA_PRODUCER = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)


def produce_message(topic, message):
    try:
        validate(instance=message, schema=get_user_role_changed_json_schema())
    except ValidationError:
        print("ochen ploho")
        # save_message_to_some_bd_to_fix_it_later(message)
    message = message.encode('utf-8')
    KAFKA_PRODUCER.send(topic, message)
