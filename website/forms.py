from django import forms

class Contact_Sales(forms.Form):
    """
    Allows potential customers to
    contact the sales team
    """
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': '201-327-3282'}))
