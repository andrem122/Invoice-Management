from django import forms
from django.forms import ModelForm
from expenses.models import House

class Add_Expense(ModelForm, forms.Form):
    """
    Allows users to add expenses to the database.
    """
    class Meta:
        model = House
        fields = ['address', 'house_list_file']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': '1234 N Drive Street'})
        }
