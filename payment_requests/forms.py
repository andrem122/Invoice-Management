from django import forms
from django.forms import ModelForm
from jobs.models import Request_Payment

#a form that has all the attributes of the Job class from the jobs app
class Approve_Payment(ModelForm, forms.Form):
    class Meta:
        model = Request_Payment
        #the attributes from the Job class that we want to exclude in our form
        #widgets for each input element
        exclude = ['job', 'amount', 'approved', 'house', 'document_link']
