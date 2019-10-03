from django import forms
from .models import Appointment
from django.views.generic.edit import CreateView, UpdateView

class AppointmentFormCreate(forms.ModelForm):
    time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])
    class Meta:
        model = Appointment
        fields = ['name', 'phone_number', 'unit_type', 'time']

class AppointmentFormUpdate(forms.ModelForm):
    time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])
    class Meta:
        model = Appointment
        fields = ['name', 'phone_number', 'unit_type', 'time']


class AppointmentCreate(CreateView):
    form_class = AppointmentFormCreate
    model = Appointment

class AppointmentUpdate(UpdateView):
    form_class = AppointmentFormUpdate
    model = Appointment
