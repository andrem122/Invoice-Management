from django import forms
from django.forms import ModelForm
from .models import Company
from django.utils.translation import gettext_lazy as _

class CompanyFormCreate(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'phone_number',
            'email',
            'days_of_the_week_enabled',
            'hours_of_the_day_enabled',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'full-width'}),
            'address': forms.TextInput(attrs={'placeholder': 'Company Address', 'class': 'full-width'}),
            'phone_number': forms.PasswordInput(attrs={'placeholder': 'Company Phone Number', 'class': 'full-width'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Company Email', 'class': 'full-width'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove labels
        self.fields['name'].label = ''
        self.fields['address'].label = ''
        self.fields['phone_number'].label = ''
        self.fields['email'].label = ''
