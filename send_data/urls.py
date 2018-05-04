from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_data, name='send_data'),
]
