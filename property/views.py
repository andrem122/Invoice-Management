from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CompanyFormCreate
from django.urls import reverse_lazy

class PropertyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Powers a form to create a new management property"""

    form_class = CompanyFormCreate
    template_name = 'property/add_property.html'
    success_message = 'Property successfully added!'
    success_url = reverse_lazy('appointments:list_appointments')

    def form_valid(self, form):
        # Associate the property added with the customer
        customer_user = self.request.user.customer_user
        customer_user.company = form.save()
        customer_user.save()
        return super().form_valid(form)
