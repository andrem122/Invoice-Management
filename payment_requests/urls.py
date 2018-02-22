from django.urls import path
from . import views

urlpatterns = [
    #example: site/job
    path('approved_payments', views.approved_payments, name='approved_payments'),
    path('unapproved_payments', views.unapproved_payments, name='unapproved_payments'),
    path('thank_you', views.thank_you, name='thank_you'),
]
