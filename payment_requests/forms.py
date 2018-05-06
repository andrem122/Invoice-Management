from django import forms
from django.forms import ModelForm
from jobs.models import Request_Payment

#a form that has all the attributes of the Request_Payment class from the jobs app
class Change_Payment_Status(ModelForm, forms.Form):
    class Meta:
        model = Request_Payment
        exclude = ['job', 'amount', 'approved', 'house', 'document_link', 'requested_by_worker']
