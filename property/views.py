from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PropertyFormCreate

class PropertyCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new management property"""

    form_class = PropertyFormCreate
    template_name = 'property/add_property.html'
    success_message = 'Property successfully added!'
