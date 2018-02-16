from django.urls import path
from . import views

urlpatterns = [
    #example: site/job
    path('', views.index, name='index'),
    path('redirect', views.redirect_user, name='redirect_user'),
    path('thank_you', views.thank_you, name='thank_you'),
]
