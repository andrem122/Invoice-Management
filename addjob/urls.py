from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_job, name='add_job'),
    #/addjob/532
    path('view_contract', views.view_contract, name='view_contract'),
]
