from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class Property(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    email = models.EmailField(max_length=100)

    def clean(self):

        if self.name == None:
            raise ValidationError(
                _('Please enter the name of the property or residence.'),
                code='FieldNotFilledOut'
            )
        if self.address == None:
            raise ValidationError(
                _('Please enter an address for the property.'),
                code='FieldNotFilledOut'
            )
        if self.phone_number == None:
            raise ValidationError(
                _('Please enter a phone number for the property.'),
                code='FieldNotFilledOut'
            )
        if self.email == None:
            raise ValidationError(
                _('Please enter an email for the property.'),
                code='FieldNotFilledOut'
            )
