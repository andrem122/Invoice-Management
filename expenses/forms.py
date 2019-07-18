from django import forms
from django.forms import ModelForm
from jobs.models import House
from .models import Expenses

class Delete_Expense(ModelForm, forms.Form):
    """
    Allows users to remove expenses from the database.
    """
    class Meta:
        model = Expenses
        exclude = [
            'house',
            'amount',
            'expense_type',
            'document_link',
            'customer',
            'submit_date',
        ]

class Edit_Expense(ModelForm, forms.Form):
    """
    Allows users to edit an expense instance
    """

    class Meta:
        model = Expenses
        fields = [
            'house',
            'amount',
            'expense_type',
            'pay_this_week',
            'description',
            'memo',
            'document_link',
        ]

        widgets = {
            'document_link': forms.FileInput(attrs={'class': 'file_upload'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #filter house by customer id
        self.fields['house'].queryset = House.objects.filter(customer=user)
