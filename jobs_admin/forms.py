from django import forms
from django.forms import ModelForm
from jobs.models import Job

#a form that has all the attributes of the Job class from the jobs app
class Change_Job_Status(ModelForm, forms.Form):
    class Meta:
        model = Job
        #the attributes from the Job class that we want to exclude in our form
        #widgets for each input element
        exclude = ['house', 'company', 'start_amount', 'start_date', 'total_paid', 'document_link', 'approved', 'balance_amount']
