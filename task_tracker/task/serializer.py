from rest_framework import serializers
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'assign', 'title', 'description', 'is_open')
        read_only_fields = ('id', 'assign', 'is_open')
