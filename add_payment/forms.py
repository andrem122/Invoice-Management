from django import forms
from django.forms import ModelForm
from jobs.models import Request_Payment

#a form that has all the attributes of the Job class from the jobs app
class Add_Payment(ModelForm, forms.Form):
    """
    Allows users to add payments to the database
    house: the property the job is at
    start_amount: the amount of money for the job
    document_link: the invoice document for the job
    """
    class Meta:
        model = Request_Payment
        fields = ['amount', 'document_link']

        #custom labels for each input
        labels = {
        }

        widgets = {
            #'document_link': forms.FileInput(attrs={'class': 'file_upload'}),
        }
