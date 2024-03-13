from django.db import migrations
from account.models import Role

ROLE_TO_SCOPES = {
    'admin': 'task:create task:read task:assign role:admin, balance:read',
    'manager': 'task:create task:read task:assign role:manager balance:read',
    'employer': 'task:create task:read task:close role:employer balance:read'
}


def create_default_role_oauth_scopes(apps, schema_editor):
    for role_name in ROLE_TO_SCOPES:
        Role.objects.get_or_create(name=role_name, scopes=ROLE_TO_SCOPES[role_name])


def remove_default_role_oauth_scopes(apps, schema_editor):
    for role_name in ROLE_TO_SCOPES:
        try:
            role = Role.objects.get(name=role_name)
            role.delete()
        except Role.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_role_oauth_scopes, remove_default_role_oauth_scopes),
    ]
