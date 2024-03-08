from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from account.logic import send_profile_role_changed
from account.models import Profile, Role


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        employer_role = Role.objects.get(name='employer')
        Profile.objects.create(user=instance, role=employer_role)


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    send_profile_role_changed(profile=instance)
