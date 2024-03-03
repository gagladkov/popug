import random

from django.conf import settings
from django.contrib.auth.models import User

from clients.kafka_client.producer import send_batched_messages, produce_message
from task.models import Task, Profile
import json


def generate_task_message(task):
    task_dict = {'task.uuid': str(task.uuid),
                 'task.title': task.title,
                 'task.description': task.description,
                 'task.is_open': task.is_open,
                 'task.assign_profile_uuid': None}
    task_message = json.dumps(task_dict)
    return task_message


def assign_tasks():
    tasks = Task.objects.filter(is_open=True)
    messages = []
    for task in tasks:
        count = Profile.objects.filter(role='employer').count()
        random_index = random.randint(0, count - 1)
        random_user = Profile.objects.filter(role='employer')[random_index]
        task.assign = random_user
        task.save()
        message = generate_task_message(task=task)
        messages.append(message)
    send_batched_messages(topic=settings.KAFKA_TOPIC_TASK_TRACKER_ASSIGNED, messages=messages)


def send_task_closed_message(task):
    message = generate_task_message(task)
    produce_message(topic=settings.KAFKA_TOPIC_TASK_TRACKER_CLOSED, message=message)


def send_task_created_message(task):
    message = generate_task_message(task)
    produce_message(topic=settings.KAFKA_TOPIC_TASK_TRACKER_CREATED, message=message)


def update_or_create_profile(profile_data):
    try:
        user = User.objects.get(username=profile_data['user.username'])
    except User.DoesNotExist:
        user = User.objects.create(username=profile_data['user.username'])

    try:
        profile = Profile.objects.get(user=user)
        profile.uuid = profile_data['profile.uuid']
        profile.role = profile_data['profile.role']
        profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=user,
                               uuid=profile_data['profile.uuid'],
                               role=profile_data['profile.role'])
