from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

#create database table structure here
class House(models.Model):
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.address

class Job(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    start_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    document_link = models.CharField(max_length=800)

    def __str__(self):
        return str(self.company.get_username()) + '-' + str(self.house.address)

    #returns a property
    #balance is calculated using the start_amount and total_paid
    @property
    def balance(self):
        if self.total_paid > self.start_amount:
            logger.error('Total amount paid exceeds the starting job amount.')
        diff = self.start_amount - self.total_paid
        #store the difference in the database as column balance
        balance = models.DecimalField(max_digits=8, decimal_places=2, default=diff)
        return diff
