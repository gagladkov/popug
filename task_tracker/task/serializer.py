from rest_framework import serializers
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'assigned_profile', 'title', 'description', 'is_open')
        read_only_fields = ('id', 'assigned_profile', 'is_open')
