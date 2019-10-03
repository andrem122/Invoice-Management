from django import forms
from .models import Appointment
from django.views.generic.edit import CreateView

class AppointmentForm(forms.ModelForm):
    time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])
    class Meta:
        model = Appointment
        fields = ['name', 'phone_number', 'unit_type', 'time']


class Appointment(CreateView):
    form_class = AppointmentForm
    model = Appointment
