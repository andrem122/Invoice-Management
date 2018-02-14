from django import forms
from django.forms import ModelForm
from jobs.models import House, Job

#a form that has all the attributes of the Job class from the jobs app
class AddJob(ModelForm, forms.Form):
    class Meta:
        model = Job

        #the attributes from the Job class that we want to exclude in our form
        exclude = ['total_paid', 'company', 'approved']

        #custom labels for each input
        labels = {
            'start_amount': 'Amount($)'
        }
