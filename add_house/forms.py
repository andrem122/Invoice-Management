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
        fields = [
            'address',
            'purchase_price',
            'profit',
            'after_repair_value',
        ]

        labels = {
            'profit': 'Desired Profit',
            'after_repair_value': 'Sell Price',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget = forms.TextInput(attrs={'placeholder': '1234 N Old Way'})
        self.fields['purchase_price'].widget = forms.NumberInput(attrs={'placeholder': '500000',})
