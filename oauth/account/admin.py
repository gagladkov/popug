from django.contrib import admin

from account.models import Role, Profile


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'scopes']


admin.site.register(Role, RoleAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'uuid', 'role']


admin.site.register(Profile, ProfileAdmin)
