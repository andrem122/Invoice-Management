from django import forms
from .models import Tenant
from django.views.generic.edit import CreateView
from django.utils.translation import gettext as _

class TenantFormCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Checks if lease length is a positive integer"""

        # Call clean method from base class first
        cleaned_data = super().clean()
        lease_length = cleaned_data.get('lease_length')
        print(type(lease_length))

        # If lease length is less than or equal to zero, raise an error
        if lease_length <= 0:
            message = 'Please choose a number larger than zero for lease length.'
            raise forms.ValidationError(_(message), 'invalid_input')

        return cleaned_data

    lease_begin = forms.DateTimeField(
        input_formats=['%m/%d/%Y'],
        widget=forms.TextInput(attrs={'onkeydown':'return false', 'readonly': 'true'}),
    )

    class Meta:
        model = Tenant
        fields = ['name', 'phone_number', 'email', 'lease_begin', 'lease_length']

class TenantMassMessage(forms.Form):
    message = forms.CharField(label='Message', max_length=1000, widget=forms.Textarea)
