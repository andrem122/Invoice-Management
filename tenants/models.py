from django.db import models
from property.models import Company
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Tenant(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    phone_number = PhoneNumberField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(null=True)
    lease_begin = models.DateField()
    lease_length = models.IntegerField(default=12) # In months

    def __str__(self):
        return 'Tenant #{0} - {1} - {2}'.format(self.pk, self.name, self.company.name)

    def get_absolute_url(self):
        return reverse('tenants:add_tenant') + '?c=' + str(self.company.id)

    @property
    def lease_end(self):
        # Calculates the end date of the lease
        # Returns: Date object
        return self.lease_begin + relativedelta(months=+self.lease_length)

    @property
    def ending_soon(self):
        # If the lease end date is within 90 days from now, returns true else returns false
        # Returns: Boolean

        # Get current date
        date_now = datetime.now().date()
        date_difference = self.lease_end - date_now
        return date_difference.days <= 90
