from django.conf import settings
from kafka import KafkaProducer


KAFKA_PRODUCER = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
BATCH_SIZE = 20


def send_batched_messages(topic, messages):
    for message in messages:
        message = message.encode('utf-8')
        KAFKA_PRODUCER.send(topic, message)
    KAFKA_PRODUCER.flush()


def produce_message(topic, message):
    message = message.encode('utf-8')
    KAFKA_PRODUCER.send(topic, message)
    KAFKA_PRODUCER.flush()
