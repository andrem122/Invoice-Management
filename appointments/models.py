from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from importlib import import_module
from datetime import datetime, timedelta
import arrow, pytz

@python_2_unicode_compatible
class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = PhoneNumberField()
    time = models.DateTimeField()

    # Additional fields not visible to users
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    #apply_task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    time_zone = TimeZoneField(default='US/Eastern', editable=False)
    confirmed = models.BooleanField(default=False)
    apartment_complex_name = models.CharField(max_length=128, blank=True, editable=False, default=None)

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
        return reverse('appointments:view_appointment', args=[str(self.id)]) + '?apartment-complex-name=' + self.apartment_complex_name

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
        now = timezone.now()
        now = now.replace(tzinfo=pytz.timezone('US/Eastern'))
        appointment_time = self.time.replace(tzinfo=pytz.timezone('US/Eastern'))
        reminder_time = appointment_time + timedelta(minutes=minutes)
        milli_to_wait = int(
            (reminder_time - now).total_seconds()
        ) * 1000

        print('MILI TO WAIT')
        print(milli_to_wait)

        # Schedule the Dramatiq task
        task_function = getattr(import_module('appointments.tasks'), task_function_name)
        result = task_function.send_with_options(
            args=(self.pk,),
            delay=milli_to_wait,
        )

        return result.message_id
