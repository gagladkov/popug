from django.conf import settings
from kafka import KafkaProducer

KAFKA_PRODUCER = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)


def produce_message(topic, message):
    message = message.encode('utf-8')
    KAFKA_PRODUCER.send(topic, message)
