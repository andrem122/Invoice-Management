from django.urls import path
from . import views

urlpatterns = [
    path('', views.expenses, name='expenses'),
]
