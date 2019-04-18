from django import forms
from django.forms import ModelForm
from jobs.models import House

#a form that has all the attributes of the Job class from the jobs app
class Archive_House(ModelForm, forms.Form):
    class Meta:
        model = House
        exclude = ['address',
                   'companies',
                   'customer',
                   'proposed_jobs',
                   'completed_jobs',
                   'rejected_jobs',
                   'payment_history',
                   'pending_payments',
                   'rejected_payments',
                   'expenses',
                   'archived',
                   'purchase_price',
                   'profit',
                   'after_repair_value',
                   'house_list_file',
                  ]
