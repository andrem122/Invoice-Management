from django import forms
from django.forms import ModelForm
from expenses.models import Expenses
from jobs.models import House

class Add_Expense(ModelForm, forms.Form):
    """
    Allows users to add expenses to the database.
    """
    class Meta:
        model = Expenses
        fields = [
            'house',
            'amount',
            'expense_type',
            'document_link',
        ]

        widgets = {
            'document_link': forms.FileInput(attrs={'class': 'file_upload'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #filter house by customer id
        self.fields['house'].queryset = House.objects.filter(customer=user, archived=False)
