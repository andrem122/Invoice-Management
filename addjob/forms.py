from django import forms
from django.forms import ModelForm
from jobs.models import House, Job

#a form that has all the attributes of the Job class from the jobs app
class AddJob(ModelForm, forms.Form):
    class Meta:
        model = Job
        fields = ['house', 'start_amount', 'document_link']

        #custom labels for each input
        labels = {
            'start_amount': 'Amount($)'
        }

    def __init__(self, user, *args, **kwargs):
        super(AddJob, self).__init__(*args, **kwargs)
        #filter house by customer id
        self.fields['house'].queryset = House.objects.filter(customer=int(user.groups.values_list('name', flat=True)[1]))
