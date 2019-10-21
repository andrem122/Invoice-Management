from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from customer_register.models import Customer_User

class Property(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    email = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer_User, on_delete=models.CASCADE)
