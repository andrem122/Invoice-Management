from django import forms
from django.forms import ModelForm
from jobs.models import Job, Request_Payment, House
from django.contrib.auth.models import User

#a form that has all the attributes of the Job class from the jobs app
class Approve_Job(ModelForm, forms.Form):
    """
    Allows users to approve a job
    """
    class Meta:
        model = Job
        #the attributes from the Job class that we want to exclude in our form
        #widgets for each input element
        exclude = [
            'house',
            'company',
            'start_amount',
            'start_date',
            'total_paid',
            'document_link',
            'approved',
            'balance_amount',
            'rejected',
            'notes',
        ]

#approve estimates as payments
class Approve_As_Payment(forms.Form):
    """
    Allows users to approve a job as a payment
    """
    pass

#reject estimates
class Reject_Estimate(forms.Form):
    """
    Allows users to reject a Job
    """
    pass


class Edit_Job(ModelForm, forms.Form):
    """
    Allows users to edit a the Job Instance
    """
    
    class Meta:
        model = Job
        fields = [
            'house',
            'company',
            'start_amount',
            'document_link',
            'notes',
        ]

        widgets = {
            'document_link': forms.FileInput(attrs={'class': 'file_upload'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #get customer id
        customer_id = user.id
        #filter house by customer id
        self.fields['house'].queryset = House.objects.filter(customer=customer_id, archived=False)
        self.fields['company'].queryset = User.objects.filter(groups=str(customer_id))
