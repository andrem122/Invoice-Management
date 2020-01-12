from django.db import models
from property.models import Property
from customer_register.models import Customer_User
from phonenumber_field.modelfields import PhoneNumberField

class Tenant(models.Model):
    customer_user = models.ForeignKey(Customer_User, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    name = models.CharField(max_length=150)
    address = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True)
    phone_number = PhoneNumberField()
    lease_begin = models.DateField()
