from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Property(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    email = models.EmailField(max_length=100)
