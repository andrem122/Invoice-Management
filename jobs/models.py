from django.db import models
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
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    start_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    document_link = models.CharField(max_length=800)

    def __str__(self):
        info = [self.house_id, self.start_amount, self.start_date]
        info = [str(x) for x in info]
        return info[0] + '-' + info[1] + '-' + info[2]

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
