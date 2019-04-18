from django.core.management.base import BaseCommand, CommandError
from sms_alerts.sms_budget_alerts import sms_budget_alerts

class Command(BaseCommand):
    help = 'Checks the budget of each house and sends SMS alerts'

    def handle(self, *args, **options):
        sms_budget_alerts()
