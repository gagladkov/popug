import json

from django.conf import settings
from kafka import KafkaConsumer

from accounting.logic import update_or_create_profile, create_task_with_prices, make_assign_credit, \
    make_close_debit


def consume_profiles_role_changed():
    consumer = KafkaConsumer(settings.KAFKA_TOPIC_PROFILES_ROLE_CHANGED, bootstrap_servers=[settings.KAFKA_SERVER])
    for message in consumer:
        profile_data = json.loads(message.value.decode('utf-8'))
        print('profile role changed:')
        print(profile_data)
        update_or_create_profile(profile_data)


def consume_task_created():
    consumer = KafkaConsumer(settings.KAFKA_TOPIC_TASK_TRACKER_CREATED, bootstrap_servers=[settings.KAFKA_SERVER])
    for message in consumer:
        task_data = json.loads(message.value.decode('utf-8'))
        print('task created:')
        print(task_data)
        create_task_with_prices(task_data)


def consume_task_assigned():
    consumer = KafkaConsumer(settings.KAFKA_TOPIC_TASK_TRACKER_ASSIGNED, bootstrap_servers=[settings.KAFKA_SERVER])
    for message in consumer:
        task_data = json.loads(message.value.decode('utf-8'))
        print('task assigned:')
        print(task_data)
        make_assign_credit(task_data)


def consume_task_closed():
    consumer = KafkaConsumer(settings.KAFKA_TOPIC_TASK_TRACKER_CLOSED, bootstrap_servers=[settings.KAFKA_SERVER])
    for message in consumer:
        task_data = json.loads(message.value.decode('utf-8'))
        print('task closed:')
        print(task_data)
        make_close_debit(task_data)
