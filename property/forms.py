from django import forms
from django.forms import ModelForm
from .models import Company, Company_Disabled_Datetimes, Company_Disabled_Days
from django.utils.translation import gettext as _

class CompanyFormCreate(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'city',
            'state',
            'zip',
            'phone_number',
            'email',
            'days_of_the_week_enabled',
            'hours_of_the_day_enabled',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'full-width'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street Address', 'class': 'full-width'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'full-width'}),
            'zip': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'full-width'}),
            'phone_number': forms.PasswordInput(attrs={'placeholder': 'Company Phone Number', 'class': 'full-width'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Company Email', 'class': 'full-width'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove labels
        self.fields['name'].label = ''
        self.fields['address'].label = ''
        self.fields['city'].label = ''
        self.fields['state'].label = ''
        self.fields['zip'].label = ''
        self.fields['phone_number'].label = ''
        self.fields['email'].label = ''

class CompanyDisabledDatetimes(forms.ModelForm):
    disabled_datetime_from = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    disabled_datetime_to = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    class Meta:
        model = Company_Disabled_Datetimes
        fields = [
            'disabled_datetime_from',
            'disabled_datetime_to',
        ]

class Company_Disabled_Days_Form(forms.ModelForm):
    class Meta:
        model = Company_Disabled_Days
        fields = [
            'disabled_days_of_the_week',
            'disabled_times_for_each_day',
        ]

        error_messages = {
            'disabled_days_of_the_week': {
                'required': _('Please choose a day of the week to disable.'),
            }, 'disabled_times_for_each_day': {
                'required': _('Please choose the hours for each day to disable.'),
            },
        }
