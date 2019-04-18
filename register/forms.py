from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

#a form that has all the attributes of the Job class from the jobs app
class Register(ModelForm):
    class Meta:
        model = User
        #widgets for each input element
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
