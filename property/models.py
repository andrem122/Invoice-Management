from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

DAYS_OF_THE_WEEK = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
)

HOURS_OF_THE_DAY = (
    (0, '12:00 AM'),
    (1, '1:00 AM'),
    (2, '2:00 AM'),
    (3, '3:00 AM'),
    (4, '4:00 AM'),
    (5, '5:00 AM'),
    (6, '6:00 AM'),
    (7, '7:00 AM'),
    (8, '8:00 AM'),
    (9, '9:00 AM'),
    (10, '10:00 AM'),
    (11, '11:00 AM'),
    (12, '12:00 PM'),
    (13, '1:00 PM'),
    (14, '2:00 PM'),
    (15, '3:00 PM'),
    (16, '4:00 PM'),
    (17, '5:00 PM'),
    (18, '6:00 PM'),
    (19, '7:00 PM'),
    (20, '8:00 PM'),
    (21, '9:00 PM'),
    (22, '10:00 PM'),
    (23, '11:00 PM'),
)

class Company(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    days_of_the_week_enabled = MultiSelectField(choices=DAYS_OF_THE_WEEK, max_choices=7, default=None)
    hours_of_the_day_enabled = MultiSelectField(choices=HOURS_OF_THE_DAY, max_choices=24, default=None)

    def __str__(self):
        return str(self.id) + '-' + self.name + '-' + self.address
