from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import logging
import os

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
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_house')

    def __str__(self):
        return self.address

    def generate_file_path(self, file_name):
        return os.path.join('customer_uploads', 'add_house', str(file_name))

    house_list_file = models.FileField(null=True, blank=True)

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
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company.get_username()) + '-' + str(self.house.address + '-' + str(self.start_amount))

    def generate_file_path(self, file_name):
        return os.path.join('worker_uploads', str(self.house.address), str(file_name))

    document_link = models.FileField(null=True, blank=True, upload_to=generate_file_path)

    #balance is calculated using start_amount and total_paid
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

    def generate_file_path(self, file_name):
        return os.path.join('customer_uploads', 'documents', str(self.job), str(file_name))

    document_link = models.FileField(null=True, blank=True, upload_to=generate_file_path)
