from django import forms
from django.forms import ModelForm
from jobs.models import House, Job
import os

#a form that has all the attributes of the Job class from the jobs app
class AddJob(ModelForm, forms.Form):
    #extra form fields we want to add not included in the Job class
    document = forms.FileField(required=True, label='Upload the invoice document')
    class Meta:
        model = Job

        #the attributes from the Job class that we want to exclude in our form
        exclude = ['total_paid', 'document_link', 'company', 'approved']

        #custom labels for each input
        labels = {
            'start_amount': 'Amount($)'
        }
