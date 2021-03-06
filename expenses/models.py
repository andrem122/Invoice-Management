from django.db import models
from django.conf import settings
from jobs.models import House
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import os

class Expenses(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_expenses')
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='expense_house', null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    submit_date = models.DateTimeField(auto_now_add=True, blank=True)
    pay_this_week = models.BooleanField(default=False)
    description = models.TextField(max_length=3000, default='', blank=True)
    memo = models.TextField(max_length=400, default='', blank=True)

    materials = 'Materials'
    no_1099 = 'No 1099'
    permits = 'Permits'
    water_bill = 'Water Bill'
    power_bill = 'Power Bill'
    misc = 'Miscellaneous'

    expense_choices = (
        (materials, 'Materials'),
        (no_1099, 'No 1099'),
        (permits, 'Permits'),
        (water_bill, 'Water Bill'),
        (power_bill, 'Power Bill'),
        (misc, 'Miscellaneous'),
    )

    expense_type = models.CharField(max_length=100, choices=expense_choices, default=materials)

    def generate_file_path(self, file_name):
        return os.path.join('customer_uploads', 'expenses', str(self.house.address), str(file_name))

    document_link = models.FileField(null=True, blank=True, upload_to=generate_file_path)

    def __str__(self):
        return str(self.house) + '-' + str(self.amount) + '-' + str(self.submit_date)

    @property
    def filename(self):
        return os.path.basename(self.document_link.name)

    def clean(self):
        """Checks that expenses added have correct data"""

        # Make sure a file is uploaded
        if self.document_link == None:
            raise ValidationError(
                _('You must upload a file for this expense.'),
                code='MissingFile'
            )

        # Make sure a property is selected
        if self.house == None:
            raise ValidationError(
                _('You must choose a property in the list.'),
                code='NoItemSelected'
            )

        # Make sure amount is greater than zero
        if self.amount <= 0:
            raise ValidationError(
                _('Expense amount must be greater than zero.'),
                code='LessThanOrEqualToZero'
            )
