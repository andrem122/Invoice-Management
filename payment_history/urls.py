from django.urls import path
from . import views

app_name = 'payment_history'
urlpatterns = [
    path('p-history-job', views.p_history_job, name='p_history_job'),
    path('thank-you', views.thank_you, name='thank_you'),
]
