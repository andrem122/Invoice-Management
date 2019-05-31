from django.urls import path
from . import views

app_name = 'csv_generator'

urlpatterns = [
    path('all-data-spreadsheet', views.all_data_spreadsheet, name='all_data_spreadsheet'),
    path('project-details-spreadsheet', views.project_details_spreadsheet, name='project_details_spreadsheet'),
]
