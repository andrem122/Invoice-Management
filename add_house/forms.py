from django import forms
from django.forms import ModelForm
from jobs.models import House

class Add_House(ModelForm, forms.Form):
    """
    Allows users to add properties to the database
    house_list_file: a user uploaded file containing the addresses
    they want added to the database
    """
    address = forms.CharField(required=False)
    class Meta:
        model = House
        fields = ['address', 'house_list_file']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': '1234 N Drive Street'})
        }
