from django import forms

class Contact_Sales(forms.Form):
    """
    Allows potential customers to
    contact the sales team
    """
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

class Contact_Support(forms.Form):
    """
    Allows a visitor or user
    to contact the support team
    """
    email   = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(label='', max_length=5000, widget=forms.TextInput(attrs={'placeholder': 'Your message...'}))
