from django.urls import path
from .views import CompanyCreateView, CompaniesListView

app_name = 'property'

urlpatterns = [
    path('add-company', CompanyCreateView.as_view(), name='add_company'),
    path('', CompaniesListView.as_view(), name='companies'),
]
