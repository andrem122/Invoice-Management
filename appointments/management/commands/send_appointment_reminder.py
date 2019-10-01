from django.core.management.base import BaseCommand, CommandError
from appointments.appointment_reminder import appointment_reminder

class Command(BaseCommand):
    help = 'Sends appointment reminders via SMS.'

    def handle(self, *args, **options):
        appointment_reminder()
