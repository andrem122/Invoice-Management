from django import forms
from django.forms import ModelForm
from jobs.models import House, Job

#a form that has all the attributes of the Job class from the jobs app
class AddJob(ModelForm):
    class Meta:
        model = Job
        exclude = ['company', 'total_paid']
