from django.urls import path
from . import views

urlpatterns = [
    path('p_history_job', views.p_history_job, name='p_history_job'),
]
