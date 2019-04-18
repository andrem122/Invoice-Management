from django import forms
from django.forms import ModelForm
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
