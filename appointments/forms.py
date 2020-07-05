from django import forms
from .models import Appointment_Base, Appointment_Real_Estate, Appointment_Medical
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import gettext as _
import arrow


def get_create_form(conditional_model, conditional_fields):
    """Get a form based on what type of customer"""
    class AppointmentFormCreate(forms.ModelForm):
        # Formatted fields
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

            address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your address'}))
            email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your email', 'type': 'email'}))

        class Meta:
            model = conditional_model
            fields = conditional_fields

        def clean(self):
            """Checks if an appointment has already been made in the future"""

            # Call clean method from base class first
            cleaned_data = super().clean()

            now = datetime.now()
            try:
                appointment = Appointment_Base.objects.filter(time__gte=now, phone_number=cleaned_data['phone_number'])
                if appointment.exists():
                    time = arrow.get(appointment[0].time).to(appointment[0].time_zone.zone)
                    message = 'You have already made an appointment for {time}.'.format(time=time.format('MM/DD/YYYY hh:mm A'))
                    raise forms.ValidationError(_(message), 'future_appointment_exists')
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
