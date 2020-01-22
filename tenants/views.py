from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tenant

class TenantListView(LoginRequiredMixin, ListView):
    """Shows users a list of tenants"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects displayed by user
        return Tenant.objects.filter(
            customer_user=self.request.user.customer_user,
        ).order_by('-name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
