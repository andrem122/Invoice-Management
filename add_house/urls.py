from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_house, name='add_house'),
]
