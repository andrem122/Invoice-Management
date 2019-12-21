from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('product', views.product, name='product'),
    path('contact-sales', views.contact_sales, name='contact_sales'),
    path('contact-support', views.contact_support, name='contact_support'),
]
