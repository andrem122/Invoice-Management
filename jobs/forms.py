from django import forms
from django.forms import ModelForm
from .models import Request_Payment

#a form that has all the attributes of the Job class from the jobs app
class Request_Payment_Form(ModelForm, forms.Form):
    class Meta:
        model = Request_Payment
        #the attributes from the Job class that we want to exclude in our form
        exclude = ['job', 'approved', 'house', 'approved_date', 'document_link', 'requested_by_worker']

        #widgets for each input element
        widgets = {
            'amount': forms.HiddenInput(attrs={'step': '0.01'}),
        }
