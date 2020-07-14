from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from importlib import import_module
from datetime import datetime, timedelta
from property.models import Company
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return 'Appointment #{0} - {1} - {2}'.format(self.pk, self.name, self.company.customer_user.user.first_name)

    def toUTC(self, datetime_object):
        # Convert to UTC time
        tz = pytz.timezone('UTC')
        return tz.normalize(datetime_object.astimezone(pytz.utc))

    def get_absolute_url(self):
        return reverse('appointments:view_appointment', args=[str(self.id)]) + '?c=' + str(self.company.id)

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
        customer_type = self.company.customer_user.customer_type

        if customer_type == 'PM':
            model_name = 'Appointment_Real_Estate'
        elif customer_type == 'MW':
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

    # Chemistry
    test_one       = 'CMP'
    test_two       = 'BMP'
    test_three     = 'Liver Profile'
    test_four      = 'Lipid Profile'
    test_five      = 'Chem 13'
    test_six       = 'Glyco Hemoglobin'
    test_seven     = 'Microalbumin Urine'

    # Urinalysis
    test_eight     =  'Urinalysis'

    # Hematology
    test_nine      = 'CBC'
    test_ten       = 'CBC With Diff'

    # Serology
    test_eleven    = 'CoVID19 Antibody IgG / IgM'
    test_twelve    = 'Mono'
    test_thirteen  = 'Influenza A & B'
    test_fourteen  = 'Strep Screen'
    test_fifthteen = 'Pregnancy Test Qualitative'

    test_type_choices = [
        (test_one, test_one),
        (test_two, test_two),
        (test_three, test_three),
        (test_four, test_four),
        (test_five, test_five),
        (test_six, test_six),
        (test_seven, test_seven),
        (test_eight, test_eight),
        (test_nine, test_nine),
        (test_ten, test_ten),
        (test_eleven, test_eleven),
        (test_twelve, test_twelve),
        (test_thirteen, test_thirteen),
        (test_fourteen, test_fourteen),
        (test_fifthteen, test_fifthteen),
    ]

    # Genders
    male = 'M'
    female = 'F'

    gender_choices = [
        ('', 'Gender'),
        (male, 'Male'),
        (female, 'Female'),
    ]

    test_type = MultiSelectField(choices=test_type_choices, max_choices=14, default=None)
    gender    = models.CharField(max_length=100, choices=gender_choices, default='',)
