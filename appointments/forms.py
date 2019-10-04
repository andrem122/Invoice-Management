from django import forms
from .models import Appointment
from django.views.generic.edit import CreateView, UpdateView

class AppointmentFormCreate(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    class Meta:
        model = Appointment
        fields = ['time', 'name', 'phone_number', 'unit_type',]

class AppointmentFormUpdate(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.TextInput(attrs={'onkeydown':'return false'}),
    )

    class Meta:
        model = Appointment
        fields = ['time', 'name', 'phone_number', 'unit_type',]
        widgets = {
            'time': forms.TextInput(attrs={'placeholder': 'name'}),
        }


class AppointmentCreate(CreateView):
    form_class = AppointmentFormCreate
    model = Appointment

class AppointmentUpdate(UpdateView):
    form_class = AppointmentFormUpdate
    model = Appointment
