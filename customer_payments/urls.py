from django.urls import path
from . import views

app_name = 'customer_payments'

urlpatterns = [
    path('', views.Customer_Payments.as_view(), name='customer_payments'),
    path('charge/', views.charge, name='charge'),
]
