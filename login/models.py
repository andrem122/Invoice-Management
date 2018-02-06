from django.db import models

class User(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=350)
    companyname = models.CharField(max_length=250, default='Company Name')

    def __str__(self):
        return self.companyname
