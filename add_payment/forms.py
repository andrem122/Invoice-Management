from django import forms
from django.forms import ModelForm
from jobs.models import Request_Payment
from django.contrib.auth.models import User

#a form that has all the attributes of the Job class from the jobs app
class Add_Payment(ModelForm, forms.Form):
    """
    Allows users to add jobs to the database
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

    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #get customer id
    #     try:
    #         customer_id = int(user.groups.values_list('name', flat=True)[1])
    #     except ValueError:
    #         customer_id = int(user.groups.values_list('name', flat=True)[0])
    #     except IndexError:
    #         print(user.username)
    #         customer_id = user.id
    #     #filter house by customer id
    #     self.fields['house'].queryset = House.objects.filter(customer=customer_id, archived=False).order_by('address')
