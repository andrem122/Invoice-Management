from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Customer_User
from django import forms

#a form that has all the attributes of the Job class from the jobs app
class User_Register(ModelForm):
    """
    Uses the User model for form fields
    """
    class Meta:
        model = User
        #widgets for each input element
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove labels
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['password'].label = ''
        self.fields['email'].label = ''

        # Make fields requried
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('There is an account with the email address already in use.')

class Customer_User_Register(ModelForm):
    """
    Uses the Customer_User model for form fields
    """
    class Meta:
        model = Customer_User
        fields = [
            'phone_number',
            'customer_type'
        ]

        #widgets for each input element
        attrs = {
            'placeholder': 'Phone Number',
            'type': 'tel',
            'required': 'false',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs=attrs),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove labels
        self.fields['phone_number'].label = ''
        self.fields['customer_type'].label = ''

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Check to see if any users already exist with this phone number.
        try:
            match = Customer_User.objects.get(phone_number=phone_number)
        except Customer_User.DoesNotExist:
            # Unable to find a user, this is fine
            return phone_number

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('There is an account with the phone number already in use.')
