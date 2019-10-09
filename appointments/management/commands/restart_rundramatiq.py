from django.core.management.base import BaseCommand, CommandError
import subprocess

class Command(BaseCommand):
    help = 'Restarts the command "python manage.py rundramatiq" command on Heroku'

    def handle(self, *args, **options):
        subprocess.call('tasks/restart_rundramatiq.sh')
