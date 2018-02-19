from django import forms
from django.forms import ModelForm
from jobs.models import House

#a form that has all the attributes of the Job class from the jobs app
class Add_House(ModelForm, forms.Form):
    class Meta:
        model = House
        fields = ['address']

        #custom labels for each input
        labels = {
            'address': '1234 N Drive Street',
        }
