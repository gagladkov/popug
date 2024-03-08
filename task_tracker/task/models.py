import uuid as uuid
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField()
    role = models.CharField(max_length=255)


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    assign = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, default=None, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_open = models.BooleanField(default=True, null=False, blank=False)
