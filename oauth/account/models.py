import uuid

from django.contrib.auth.models import Group, User
from django.db import models


class Role(models.Model):  # роли предзаполняю в миграции, в дальнейшем кажется удобнее будет рулить правами
    name = models.CharField(max_length=255)
    scopes = models.TextField()


class Profile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
