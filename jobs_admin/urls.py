from django.urls import path
from . import views

app_name = 'jobs_admin'
urlpatterns = [
    path('', views.index, name='index'),
]
