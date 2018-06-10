from django.urls import path
from . import views

urlpatterns = [
    path('', views.payments, name='payments'),
    path('thank_you', views.thank_you, name='thank_you'),
]
