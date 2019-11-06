from django.urls import path
from . import views

app_name = 'customer_register'

urlpatterns = [
    path('', views.customer_register, name='customer-register'),
]
