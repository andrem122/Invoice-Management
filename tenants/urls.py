from django.urls import path
from .views import (
    TenantListView,
    TenantCreateView,
    TenantDeleteView,
    ProcessSendMassMessageForm,
)

app_name = 'tenants'

urlpatterns = [
    path('', TenantListView.as_view(), name='list_tenants'),
    path('add-tenant', TenantCreateView.as_view(), name='add_tenant'),
    path('delete-tenant', TenantDeleteView.as_view(), name='delete_tenant'),
    path('send-mass-message', ProcessSendMassMessageForm.as_view(), name='send_mass_message'),
]
