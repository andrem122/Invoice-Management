from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from utils.utils import get_succeeded

class Customer_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paying = models.BooleanField(default=False, editable=False)
    wants_sms = models.BooleanField(default=False)
    wants_email_notifications = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)

    house_flipper    = 'HF'
    property_manager = 'PM'
    medical_worker   = 'MW'

    customer_types = (
        (house_flipper, 'House Flipper'),
        (property_manager, 'Property Manager'),
        (medical_worker, 'Medical Worker'),
    )

    customer_type = models.CharField(max_length=100, choices=customer_types, default=house_flipper)

    def __str__(self):
        return self.user.first_name + '-' + self.user.last_name + '-' + str(self.user.id)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        Customer_User.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.groups.filter(name__in=['Customers', 'Customers Staff']).exists() and get_succeeded(Customer_User, user=instance):
        instance.customer_user.save()

ios = 'iOS'
android  = 'Android'

mobile_device_choices = (
    ('', 'Mobile Device Type'),
    (ios, 'iOS'),
    (android, 'Android'),
)

class Customer_User_Push_Notification_Tokens(models.Model):
    # One customer user can have many tokens from different devices
    # Each device gets its own token but can be tied to the same customer_user account
    device_token = models.CharField(max_length=300, null=True)
    customer_user = models.ForeignKey(Customer_User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, choices=mobile_device_choices, default='')

    def __str__(self):
        return self.customer_user.user.first_name + '-' + self.customer_user.user.last_name + '-' + str(self.device_token)
