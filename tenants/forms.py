from django import forms
from .models import Tenant
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import gettext as _
import arrow

class TenantFormCreate(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'address', 'phone_number', 'lease_begin',]

    def clean(self):
        """Checks if a tenant has already been made"""

        # Call clean method from base class first
        cleaned_data = super().clean()

        now = datetime.now()
        try:
            tenant = Tenant.objects.filter(phone_number=cleaned_data['phone_number'])
            if tenant.exists():
                message = 'You have already added {name} as a tenant.'.format(name=cleaned_data['name'])
                raise forms.ValidationError(_(message), 'object_exists')
        except KeyError:
            pass

        return cleaned_data

# class TenantFormUpdate(forms.ModelForm):
#     class Meta:
#         model = Tenant
#         fields = ['name', 'address', 'phone_number', 'lease_begin',]

class TenantCreate(CreateView):
    form_class = TenantFormCreate
    model = Tenant

class TenantUpdate(UpdateView):
    form_class = TenantFormCreate
    model = Tenant
