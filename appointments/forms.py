from django import forms
from .models import Appointment_Base, Appointment_Real_Estate, Appointment_Medical
from property.models import Company, Company_Disabled_Days, Company_Disabled_Datetimes
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import gettext as _
import arrow


def get_create_form(conditional_model, conditional_fields):
    """Get a form based on what type of customer"""
    class AppointmentFormCreate(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            super().__init__(*args, **kwargs)

        # Format the input for fields
        time = forms.DateTimeField(
            input_formats=['%m/%d/%Y %I:%M %p'],
            widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
        )
        name = forms.CharField(label='Full name', widget=forms.TextInput(attrs={'placeholder':'Full name'}))
        phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your phone number', 'type': 'tel'}))

        if conditional_model == Appointment_Medical:
            date_of_birth = forms.DateField(
                input_formats=['%m/%d/%Y'],
                widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
            )

            # Genders
            male = 'M'
            female = 'F'

            gender_choices = [
                (male, 'Male'),
                (female, 'Female'),
            ]

            gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect)
            address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your address'}))
            city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City'}))
            email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your email', 'type': 'email'}))

        elif conditional_model == Appointment_Real_Estate:
            # Categories
            three_bed = '3 Bedrooms'
            two_bed   = '2 Bedrooms'
            one_bed   = '1 Bedroom'

            unit_type_choices = (
                (three_bed, '3 Bedrooms'),
                (two_bed, '2 Bedrooms'),
                (one_bed, '1 Bedroom'),
            )

            unit_type = forms.ChoiceField(choices=unit_type_choices, widget=forms.RadioSelect)
        class Meta:
            model = conditional_model
            fields = conditional_fields

        def clean(self):
            """Checks if an appointment has already been made in the future"""

            # Call clean method from base class first
            cleaned_data = super().clean()

            # Check if the appointment conflicts with disabled times
            company_id = int(self.request.GET.get('c', None))
            company = Company.objects.get(pk=company_id)

            # Get company disabled days
            company_disabled_days_object = Company_Disabled_Days.objects.filter(company=company)

            # Get day and hour of the appointment to compare it with the disabled days and hours
            appointment_time = cleaned_data['time']
            appointment_day = appointment_time.strftime('%w')
            appointment_hour = appointment_time.strftime('%-H')

            for company_disabled_days in company_disabled_days_object:
                disabled_days_of_the_week = company_disabled_days.disabled_days_of_the_week
                disabled_times_for_each_day = company_disabled_days.disabled_times_for_each_day
                if appointment_day in disabled_days_of_the_week and appointment_hour in disabled_times_for_each_day:
                    message = 'This time is unavailable. Please choose a different time.'
                    raise forms.ValidationError(_(message), 'time_unavailable')
                    break


            now = datetime.now()
            try:
                appointment = Appointment_Base.objects.filter(time__gte=now, phone_number=cleaned_data['phone_number'])
                if appointment.exists():
                    time = arrow.get(appointment[0].time).to(appointment[0].time_zone.zone)
                    message = 'You have already made an appointment for {time}.'.format(time=time.format('MM/DD/YYYY hh:mm A'))
                    raise forms.ValidationError(_(message), 'appointment_already_made')
            except KeyError:
                pass

            return cleaned_data

    return AppointmentFormCreate

class AppointmentFormUpdate(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    class Meta:
        model = Appointment_Real_Estate
        fields = ['time', 'name', 'phone_number', 'unit_type',]
