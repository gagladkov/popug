import random
from datetime import datetime

from django.contrib.auth.models import User

from accounting.models import Task, Profile, Transaction, BillingCycle


def get_current_billing_cycle():
    try:
        bc = BillingCycle.objects.get(is_current=True)
    except BillingCycle.DoesNotExist:
        bc = BillingCycle.objects.create(is_current=True)
    return bc


def generate_assign_price():
    return random.randint(10, 20)


def generate_close_price():
    return random.randint(20, 40)


def get_company_profile():
    return Profile.objects.get(is_company=True)


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


def make_assign_credit(task_data):
    try:
        task = Task.objects.get(uuid=task_data['task.uuid'])
    except Task.DoesNotExist:
        profile = Profile.objects.get(task_data['assigned_user_uuid'])
        task = Task.objects.create(uuid=task_data['uuid'],
                                   title=task_data['title'],
                                   assigned_profile=profile,
                                   description=task_data['description'],
                                   is_open=task_data['is_open'],
                                   assign_price=generate_assign_price(),
                                   close_price=generate_close_price())

    description = f"Minus for assign task: {task.title}"
    transaction = Transaction.objects.create(profile=task.assigned_profile,
                                             credit=task.assign_price,
                                             description=description,
                                             billing_cycle=get_current_billing_cycle())
    task.assigned_profile.balance -= transaction.credit
    task.assigned_profile.save()

    company_profile = get_company_profile()
    Transaction.objects.create(profile=company_profile,
                               debit=transaction.balance,
                               description=description,
                               billing_cycle=get_current_billing_cycle())
    company_profile.balance += transaction.credit
    company_profile.save()


def make_close_debit(task_data):
    task = Task.objects.get(uuid=task_data['task.uuid'])
    task.closed_at = datetime.now()
    task.save()

    description = f"Plus for close task: {task.title}"
    transaction = Transaction.objects.create(profile=task.assigned_profile,
                                             debit=task.close_price,
                                             description=description,
                                             billing_cycle=get_current_billing_cycle())
    task.assigned_profile.balance += transaction.debit
    task.assigned_profile.save()

    company_profile = get_company_profile()
    Transaction.objects.create(profile=company_profile,
                               credit=transaction.balance,
                               description=description,
                               billing_cycle=get_current_billing_cycle())
    company_profile.balance -= transaction.debit
    company_profile.save()
