from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('proposed_jobs', views.proposed_jobs, name='proposed_jobs'),
]
