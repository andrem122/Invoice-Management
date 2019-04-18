from django import forms
from django.forms import ModelForm
from .models import Request_Payment

#a form that has all the attributes of the Job class from the jobs app
class Request_Payment_Form(ModelForm, forms.Form):
    class Meta:
        model = Request_Payment
        #the attributes from the Job class that we want to exclude in our form
        fields = ['amount', 'document_link']

        #widgets for each input element
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'document_link': forms.FileInput(attrs={'class': 'file_upload'}),
        }
