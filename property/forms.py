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

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Property Name'}),
            'address': forms.TextInput(attrs={'placeholder': 'Property Address'}),
            'phone_number': forms.PasswordInput(attrs={'placeholder': 'Property Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Property Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove labels
        self.fields['name'].label = ''
        self.fields['address'].label = ''
        self.fields['phone_number'].label = ''
        self.fields['email'].label = ''
