from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CompanyFormCreate, CompanyDisabledDatetimes
from django.urls import reverse_lazy
from .models import Company

class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Powers a form to create a new company"""

    form_class = CompanyFormCreate
    template_name = 'property/add_company.html'
    success_message = 'Property successfully added!'
    success_url = reverse_lazy('appointments:list_appointments')

    def form_valid(self, form):
        # Associate the company added with the customer
        customer_user = self.request.user.customer_user
        company = form.save()
        company.customer_user = customer_user
        return super().form_valid(form)

class CompaniesListView(LoginRequiredMixin, ListView):
    """Shows users a list of companies"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects displayed by user
        return Company.objects.filter(
            customer_user=self.request.user.customer_user
        ).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_user = self.request.user.customer_user
        context['fields'] = ('Name', 'Address', 'City', 'State', 'Phone', 'Email') # fields to show in table header
        context['customer_user'] = customer_user
        return context

class CompanyDisabledDatetimesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Allows users to add additional disabled datetimes"""
    form_class = CompanyDisabledDatetimes
    template_name = 'property/add_company_disabled_datetimes.html'
    success_message = 'Disabled date and time successfully added!'
    success_url = reverse_lazy('property:add_company_disabled_datetimes')
