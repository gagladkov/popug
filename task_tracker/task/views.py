from oauth2_provider.oauth2_validators import AccessToken

from rest_framework import status

from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from task.logic import assign_tasks, send_task_closed_message
from task.models import Task
from task.serializer import TaskSerializer
from task_tracker import settings


class TaskList(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['task:read']
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        token = AccessToken.objects.get(token=request.auth)
        scopes = token.scope

        # только 3 роли, кроме работников - менеджер и админ могут смотреть все
        if 'role:employer' in scopes.split():
            queryset = Task.objects.filter(assigned_profile=token.user.profile)
        else:
            queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCreate(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['task:create']
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            assign_tasks(topic=settings.KAFKA_TOPIC_TASK_TRACKER_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskClose(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['task:close', 'role:employer']
    allowed_methods = ['post']

    def post(self, request, pk, *args, **kwargs):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.is_open = False
        task.save()
        send_task_closed_message(task=task)
        return Response({'status': 'Task closed.'}, status=status.HTTP_200_OK)


class TaskShuffle(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['task:shuffle']
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        assign_tasks(topic=settings.KAFKA_TOPIC_TASK_TRACKER_ASSIGNED)
        return Response({'status': 'Tasks have been assigned.'}, status=status.HTTP_200_OK)
