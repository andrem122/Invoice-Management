from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from importlib import import_module

import redis, arrow, os

@python_2_unicode_compatible
class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = PhoneNumberField()
    time = models.DateTimeField()

    # Additional fields not visible to users
    appointment_task_id = models.CharField(max_length=50, blank=True, editable=False)
    apply_task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    time_zone = TimeZoneField(default='US/Eastern', editable=False)
    confirmed = models.BooleanField(default=False)

    #categories
    three_bed = '3 Bedrooms'
    two_bed   = '2 Bedrooms'
    one_bed   = '1 Bedroom'

    unit_type_choices = (
        ('', 'Unit Type'),
        (three_bed, '3 Bedrooms'),
        (two_bed, '2 Bedrooms'),
        (one_bed, '1 Bedroom'),
    )

    unit_type = models.CharField(max_length=100, choices=unit_type_choices, default='',)


    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('appointments:view_appointment', args=[str(self.id)])

    def clean(self):
        """Checks that appointments are not scheduled in the past"""

        appointment_time = arrow.get(self.time).to('UTC')

        if appointment_time < arrow.utcnow():
            raise ValidationError(
                'You cannot schedule an appointment for the past. '
                'Please check your time.')

    def schedule_reminder(self, task_function_name, minutes):
        """Schedule a Dramatiq task to send a reminder via SMS"""

        # Calculate the correct time to send this reminder
        appointment_time = arrow.get(self.time, self.time_zone.zone)
        reminder_time = appointment_time.shift(minutes=minutes)
        now = arrow.now(self.time_zone.zone)
        milli_to_wait = int(
            (reminder_time - now).total_seconds()) * 1000

        # Schedule the Dramatiq task
        task_function = getattr(import_module('appointments.tasks'), task_function_name)
        result = task_function.send_with_options(
            args=(self.pk,),
            delay=milli_to_wait
        )

        return result.options['eta']

    def save(self, *args, **kwargs):
        """Custom save method which also schedules a reminder"""

        # Check if we have scheduled an appointment reminder for this appointment before
        if self.appointment_task_id:
            # Revoke that task in case its time has changed
            self.cancel_task(self.appointment_task_id)

        if self.apply_task_id:
            self.cancel_task(self.apply_task_id)

        # Save our appointment, which populates self.pk,
        # which is used in schedule_reminder
        super().save(*args, **kwargs)

        # Schedule a new reminder task
        self.appointment_task_id = self.schedule_reminder('send_appointment_reminder', -60)
        self.apply_task_id = self.schedule_reminder('send_application_reminder', +30)

        # Save our appointment again, with the new task_ids
        super().save(*args, **kwargs)

    def cancel_task(self, task_id):
        if settings.DEBUG == True:
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            redis_client.hdel("dramatiq:default.DQ.msgs", task_id)
        else:
            redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
            redis_client = redis.from_url(redis_url)
            redis_client.hdel("dramatiq:default.DQ.msgs", task_id)
