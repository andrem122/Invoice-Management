from django.urls import path
from . import views

app_name = 'customer_register'

urlpatterns = [
    path('', views.register, name='customer-register'),
]
