from django.urls import path
from . import views

urlpatterns = [
    path('reply-call', views.incoming_call, name='incoming_call'),
    path('reply-sms', views.incoming_sms, name='incoming_sms'),
]
