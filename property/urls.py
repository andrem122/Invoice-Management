from django.urls import path
from .views import CompanyCreateView, CompaniesListView, CompanyDisabledDatetimesCreateView

app_name = 'property'

urlpatterns = [
    path('add-company', CompanyCreateView.as_view(), name='add_company'),
    path('add-company-disabled-datetimes', CompanyDisabledDatetimesCreateView.as_view(), name='add_company_disabled_datetimes'),
    path('', CompaniesListView.as_view(), name='companies'),
]
