from django import forms
from django.forms import ModelForm
from .models import Property
from django.utils.translation import gettext_lazy as _

class PropertyFormCreate(forms.ModelForm):

    class Meta:
        model = Property
        fields = '__all__'

        labels = {
            'name': _('Property Name'),
            'address': _('Property Address'),
            'phone_number': _('Property Phone'),
            'email': _('Property Email'),
        }
