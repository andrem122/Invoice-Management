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
from customer_register.models import Customer_User
import arrow, pytz

@python_2_unicode_compatible
class Appointment_Base(models.Model):
    name = models.CharField(max_length=150)
    phone_number = PhoneNumberField()
    time = models.DateTimeField()

    # Additional fields not visible to users
    created = models.DateTimeField(auto_now_add=True)
    time_zone = TimeZoneField(default='US/Eastern', editable=False)
    appointment_task_id = models.CharField(max_length=50, blank=True, editable=False)
    confirmed = models.BooleanField(default=False)
    customer_user = models.ForeignKey(Customer_User, on_delete=models.CASCADE, null=True, blank=True, editable=False)


    def __str__(self):
        return 'Appointment #{0} - {1} - {2}'.format(self.pk, self.name, self.customer_user.user.first_name)

    def toUTC(self, datetime_object):
        # Convert to UTC time
        tz = pytz.timezone('UTC')
        return tz.normalize(datetime_object.astimezone(pytz.utc))

    def get_absolute_url(self):
        return reverse('appointments:view_appointment', args=[str(self.id)]) + '?c=' + str(self.customer_user.id)

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
        appointment_time = self.toUTC(self.time)
        reminder_time = appointment_time + timedelta(minutes=minutes)
        milli_to_wait = int(
            (reminder_time - now).total_seconds()
        ) * 1000

        # Schedule the Dramatiq task
        # Get the appointment model to query when sending a text message with appointment details based on customer type

        model_name = 'Appointment_Base'
        if self.customer_user.customer_type == 'PM':
            model_name = 'Appointment_Real_Estate'
        elif self.customer_user.customer_type == 'MW':
            model_name = 'Appointment_Medical'

        task_function = getattr(import_module('appointments.tasks'), task_function_name)
        result = task_function.send_with_options(
            args=(self.pk, model_name),
            delay=milli_to_wait,
        )

        return result.message_id

@python_2_unicode_compatible
class Appointment_Real_Estate(Appointment_Base):

    # Additional fields not visible to users
    apply_task_id = models.CharField(max_length=50, blank=True, editable=False)

    # Categories
    three_bed = '3 Bedrooms'
    two_bed   = '2 Bedrooms'
    one_bed   = '1 Bedroom'

    unit_type_choices = (
        ('', 'Unit Type'),
        (three_bed, '3 Bedrooms'),
        (two_bed, '2 Bedrooms'),
        (one_bed, '1 Bedroom'),
    )

    # Additional fields that ARE visible to users
    unit_type = models.CharField(max_length=100, choices=unit_type_choices, default='',)

class Appointment_Medical(Appointment_Base):

    # Additional fields that ARE visible to users
    address = models.CharField(max_length=255, default='')
    email = models.EmailField()
    date_of_birth = models.DateField()


    # Test Types
    test_one       = 'Comprehensive Metabolic Panel'
    test_two       = 'Basic Metabolic Panel'
    test_three     = 'Lipid Panel'
    test_four      = 'Lipid Panel Plus'
    test_five      = 'Liver Panel Plus'
    test_six       = 'General Chemistry 6'
    test_seven     = 'General Chemistry 13'
    test_eight     = 'Electrolyte Panel'
    test_nine      = 'Kidney Check'
    test_ten       = 'Renal Function Panel'
    test_eleven    = 'MetLyte 8 Panel'
    test_twelve    = 'Hepatic Function Panel'
    test_thirteen  = 'Basic Metabolic Panel Plus'
    test_fourteen  = 'MetLyte Plus CRP'
    test_fifthteen = 'Biochemistry Panel Plus'
    test_sixteen   = 'MetLac 12 Panel'

    test_type_choices = [
        ('', 'Test Type'),
        (test_one, 'Comprehensive Metabolic Panel'),
        (test_two, 'Basic Metabolic Panel'),
        (test_three, 'Lipid Panel'),
        (test_four, 'Lipid Panel Plus'),
        (test_five, 'Liver Panel Plus'),
        (test_six, 'General Chemistry 6'),
        (test_seven, 'General Chemistry 13'),
        (test_eight, 'Electrolyte Panel'),
        (test_nine, 'Kidney Check'),
        (test_ten, 'Renal Function Panel'),
        (test_eleven, 'MetLyte 8 Panel'),
        (test_twelve, 'Hepatic Function Panel'),
        (test_thirteen, 'Basic Metabolic Panel Plus'),
        (test_fourteen, 'MetLyte Plus CRP'),
        (test_fifthteen, 'Biochemistry Panel Plus'),
        (test_sixteen, 'MetLac 12 Panel'),
    ]

    # Genders
    male = 'M'
    female = 'F'

    gender_choices = [
        ('', 'Gender'),
        (male, 'Male'),
        (female, 'Female'),
    ]

    test_type = models.CharField(max_length=100, choices=test_type_choices, default='',)
    gender    = models.CharField(max_length=100, choices=gender_choices, default='',)
