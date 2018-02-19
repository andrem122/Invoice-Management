from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

#create database table structure here
class House(models.Model):
    address = models.CharField(max_length=250)
    companies = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Current_Worker')
    proposed_jobs = models.BooleanField(default=False)
    pending_payments = models.BooleanField(default=False)
    payment_history = models.BooleanField(default=False)
    completed_jobs = models.BooleanField(default=False)

    def __str__(self):
        return self.address

#the class that shows if the current company has at least one job in a house
class Current_Worker(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company) + '-' + str(self.house)

class Job(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company.get_username()) + '-' + str(self.house.address)

    def generate_filename(self, filename):
        file_path = 'uploads/{}/{}'.format(str(self.house.address), str(filename))
        return file_path

    document_link = models.FileField(upload_to=generate_filename)

    #balance is calculated using the start_amount and total_paid
    @property
    def balance(self):
        if self.total_paid > self.start_amount:
            logger.error('Total amount paid exceeds the starting job amount.')
        return float(self.start_amount) - float(self.total_paid)

    balance_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class Request_Payment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True, blank=True)
    approved_date = models.DateTimeField(auto_now_add=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    approved = models.BooleanField(default=False)

    def __str__(self):
        info = [self.job.company, self.amount, self.approved]
        info = [str(x) for x in info]

        return info[0] + '-' + info[1] + '-' + info[2]

    def generate_filename(self, filename):
        file_path = 'admin_uploads/{}/{}'.format(str(self.job), str(filename))
        return file_path

    document_link = models.FileField(upload_to=generate_filename)
