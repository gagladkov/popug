from django.core.management import BaseCommand

from accounting.models import Profile
from accounting.payments import make_payload_to_profile_card, create_new_billing_cycle


class Command(BaseCommand):
    def handle(self, *args, **options):
        _process_billing_cycle()


def _process_billing_cycle():
    for profile in Profile.objects.filter(is_company=False):
        make_payload_to_profile_card(profile)
    create_new_billing_cycle()
