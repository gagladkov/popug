# Generated by Django 5.0.2 on 2024-03-08 19:47

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('role', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_open', models.BooleanField(default=True)),
                ('assign', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='task.profile')),
            ],
        ),
    ]