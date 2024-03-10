from django.contrib import admin
from django.urls import path

from task.views import TaskList, TaskCreate, TaskClose, TaskShuffle

urlpatterns = [
    path('tasks/', TaskList.as_view()),
    path('create_tasks/', TaskCreate.as_view()),
    path('close_tasks/<pk>', TaskClose.as_view()),
    path('shuffle_tasks/', TaskShuffle.as_view()),
]
