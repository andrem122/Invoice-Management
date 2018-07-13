from django.db import models
from django.conf import settings
from jobs.models import House
import os

class Expenses:
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_expenses')
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    submit_date = models.DateTimeField(auto_now_add=True, blank=True)

    materials = 'MATERIALS'
    no_1099 = 'NO 1099'
    permits = 'PERMITS'
    misc = 'MISCELLANEOUS'

    expense_choices = (
        (materials, 'Materials'),
        (no_1099, 'No 1099'),
        (permits, 'Permits'),
        (misc, 'Miscellaneous'),
    )

    expense_type = models.CharField(max_length=100, choices=expense_choices, default=materials)

    def generate_file_path(self, file_name):
        return os.path.join('customer_uploads', str(self.customer.id) + '-expenses', str(file_name))

    document_link = models.FileField(null=True, blank=True, upload_to=generate_file_path)
