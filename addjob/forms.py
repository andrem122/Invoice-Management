from django import forms
from django.forms import ModelForm
from jobs.models import House, Job

#a form that has all the attributes of the Job class from the jobs app
class AddJob(ModelForm, forms.Form):
    """
    Allows users to add jobs to the database
    house: the property the job is at
    start_amount: the amount of money for the job
    document_link: the invoice document for the job
    """
    class Meta:
        model = Job
        fields = ['house', 'start_amount', 'document_link']

        #custom labels for each input
        labels = {
            'house': 'House Address',
            'start_amount': 'Job Amount',
            'document_link': 'Job Document',
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #get customer id
        customer_id = user.groups.values_list('name', flat=True)[0]
        if customer_id == 'Workers':
            customer_id = int(user.groups.values_list('name', flat=True)[1])
        #filter house by customer id
        self.fields['house'].queryset = House.objects.filter(customer=customer_id, archived=False)
