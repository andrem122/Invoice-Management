from django import forms
from jobs.models import House

class AddJob(forms.Form):
    #get all houses as a queryset
    houses = House.objects.all()
    time = forms.DateTimeField(widget=forms.HiddenInput())
    house = forms.ModelMultipleChoiceField(required=True, queryset=houses)
    start_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    document = forms.FileField(label='Upload the invoice document')
