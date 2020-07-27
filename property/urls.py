from django.urls import path
from .views import CompanyCreateView, CompaniesListView, CompanyDisabledDatetimesCreateView, CompanyDisabledDatetimesListView, CompanyDisabledDatetimesDeleteView, CompanyDisabledDaysListView, CompanyDisabledDaysDeleteView

app_name = 'property'

urlpatterns = [
    path('add-company', CompanyCreateView.as_view(), name='add_company'),
    path('add-company-disabled-datetimes', CompanyDisabledDatetimesCreateView.as_view(), name='add_company_disabled_datetimes'),
    path('delete-company-disabled-datetimes', CompanyDisabledDatetimesDeleteView.as_view(), name='delete_company_disabled_datetimes'),
    path('delete-company-disabled-days', CompanyDisabledDaysDeleteView.as_view(), name='delete_company_disabled_days'),
    path('company-disabled-datetimes', CompanyDisabledDatetimesListView.as_view(), name='list_company_disabled_datetimes'),
    path('company-disabled-days', CompanyDisabledDaysListView.as_view(), name='list_company_disabled_days'),
    path('', CompaniesListView.as_view(), name='companies'),
]
