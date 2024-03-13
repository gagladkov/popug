from accounting.logic import get_current_billing_cycle, get_company_profile
from accounting.models import BillingCycle, Profile, Transaction


def make_payload_to_profile_card(profile):
    if profile.balance > 0:
        # make transaction payload
        # amount = profile.balance
        # client.payment.pay(profile.card, amount)
        description = "Payload to profile"
        Transaction.objects.create(profile=profile,
                                   credit=profile.balance,
                                   description=description)
        profile.balance = 0
        profile.save()
        # client.mail.send_check(profile, amount)


def create_new_billing_cycle():
    # process_company_money()
    current_billing_cycle = get_current_billing_cycle()
    current_billing_cycle.is_current = False
    company_profile = get_company_profile()
    current_billing_cycle.company_balance = company_profile.balance
    company_profile.balance = 0
    company_profile.save()
    BillingCycle.objects.create()
