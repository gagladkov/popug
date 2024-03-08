from django.contrib import admin

from task.models import Task, Profile


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'assign', 'is_open']


admin.site.register(Task, TaskAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'role', 'user']


admin.site.register(Profile, ProfileAdmin)
