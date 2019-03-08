from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from utils.utils import get_succeeded

class Customer_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paying = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        Customer_User.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.groups.filter(name__in=['Customers', 'Customers Staff']).exists() and get_succeeded(Customer_User, user=instance):
        instance.customer_user.save()
