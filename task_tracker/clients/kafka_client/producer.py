from django.conf import settings
from kafka import KafkaProducer
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from clients.kafka_client.json_schema_loader import get_json_schema

KAFKA_PRODUCER = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
BATCH_SIZE = 20

def send_batched_messages(topic, messages):
    for message in messages:
        message = message.encode('utf-8')
        try:
            validate(instance=message, schema=get_json_schema(topic_name=topic))
        except ValidationError:
            print("ochen ploho")
            # save_message_to_some_bd_to_fix_it_later(message)
        KAFKA_PRODUCER.send(topic, message)
    KAFKA_PRODUCER.flush()


def produce_message(topic, message):
    message = message.encode('utf-8')
    try:
        validate(instance=message, schema=get_json_schema(topic_name=topic))
    except ValidationError:
        print("ochen ploho")
        # save_message_to_some_bd_to_fix_it_later(message)
    KAFKA_PRODUCER.send(topic, message)
    KAFKA_PRODUCER.flush()
