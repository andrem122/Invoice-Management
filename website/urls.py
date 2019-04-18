from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='register'),
    path('contact-sales', views.contact_sales, name='contact_sales'),
]
