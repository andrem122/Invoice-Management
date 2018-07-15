from django import forms
from django.forms import ModelForm
from expenses.models import Expenses

class Add_Expense(ModelForm, forms.Form):
    """
    Allows users to add expenses to the database.
    """
    class Meta:
        model = Expenses
        fields = ['house', 'amount', 'expense_type', 'document_link']
