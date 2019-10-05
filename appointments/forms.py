from django import forms
from .models import Appointment
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import gettext as _
import arrow

class AppointmentFormCreate(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    class Meta:
        model = Appointment
        fields = ['time', 'name', 'phone_number', 'unit_type',]

    def clean(self):
        """Checks if an appointment has already been made in the future"""

        # Call clean method from base class first
        cleaned_data = super().clean()
        print(cleaned_data)

        now = datetime.now()
        try:
            appointment = Appointment.objects.filter(time__gte=now, phone_number=cleaned_data['phone_number'])
            if appointment.exists():
                time = arrow.get(appointment[0].time).to(appointment[0].time_zone.zone)
                message = 'You have already made an appointment for {time}.'.format(time=time.format('MM/DD/YYYY hh:mm A'))
                raise forms.ValidationError(_(message), 'future_appointment_exists')
        except KeyError:
            pass

        return cleaned_data

class AppointmentFormUpdate(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    class Meta:
        model = Appointment
        fields = ['time', 'name', 'phone_number', 'unit_type',]

class AppointmentCreate(CreateView):
    form_class = AppointmentFormCreate
    model = Appointment

class AppointmentUpdate(UpdateView):
    form_class = AppointmentFormUpdate
    model = Appointment
