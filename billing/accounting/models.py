import uuid as uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField()
    role = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)
    is_company = models.BooleanField(default=False, editable=False)


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    assigned_profile = models.ForeignKey(to=Profile, default=None, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, editable=False)
    is_open = models.BooleanField(default=True)
    closed_at = models.DateTimeField(null=True, default=None)
    assign_price = models.IntegerField(editable=False)
    close_price = models.IntegerField(editable=False)


class BillingCycle(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, db_index=True)
    company_balance = models.IntegerField(default=0, editable=False)


class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, editable=False)
    description = models.CharField(max_length=255, editable=False)
    credit = models.IntegerField(default=0, editable=False)
    debit = models.IntegerField(default=0, editable=False)
    billing_cycle = models.ForeignKey(BillingCycle, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, db_index=True)
