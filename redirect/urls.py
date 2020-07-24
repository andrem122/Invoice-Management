from django.urls import path
from . import views

app_name = 'redirect'

urlpatterns = [
    path('login', views.redirect_login, name='redirect_login'),
]
