import random
from datetime import datetime

from django.contrib.auth.models import User

from accounting.models import Task, Profile, Transaction, BillingCycle


def get_current_billing_cycle():
    return BillingCycle.objects.get(is_current=True)


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


def create_task_with_prices(task_data):
    assign_price = random.randint(10, 20)
    close_price = random.randint(20, 40)
    Task.objects.create(uuid=task_data['task.uuid'],
                        title=task_data['task.title'],
                        assign_price=assign_price,
                        close_price=close_price)


def make_assign_credit(task_data):
    try:
        task = Task.objects.get(uuid=task_data['task.uuid'])
        description = f"Minus for assign task: {task.title}"
        transaction = Transaction.objects.create(profile=task.assign,
                                                 credit=task.assign_price,
                                                 description=description)
        task.assign.balance -= transaction.credit
        task.assign.save()

        company_profile = get_company_profile()
        Transaction.objects.create(profile=company_profile,
                                   debit=transaction.balance,
                                   description=description)
        company_profile.balance += transaction.credit
        company_profile.save()
    except Task.DoesNotExist:
        return


def make_close_debit(task_data):
    try:
        task = Task.objects.get(uuid=task_data['task.uuid'])
        task.closed_at = datetime.now()
        task.save()
        description = f"Plus for close task: {task.title}"
        transaction = Transaction.objects.create(profile=task.assign,
                                                 debit=task.close_price,
                                                 description=description)
        task.assign.balance += transaction.debit
        task.assign.save()

        company_profile = get_company_profile()
        Transaction.objects.create(profile=company_profile,
                                   credit=transaction.balance,
                                   description=description)
        company_profile.balance -= transaction.debit
        company_profile.save()
    except Task.DoesNotExist:
        return
