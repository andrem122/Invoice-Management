from django.conf.urls import re_path, include, url
from django.urls import path
from django.contrib import admin

from .views import (
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    incoming_sms,
)

app_name = 'appointments'


urlpatterns = [
    # Here we add our Twilio URLs
    url(r'^incoming-sms/$', incoming_sms, name='incoming_sms'),
    # List and detail views
    url(r'^$', AppointmentListView.as_view(), name='list_appointments'),
    url(r'^(?P<pk>[0-9]+)$',
            AppointmentDetailView.as_view(),
            name='view_appointment'),

    # Create, update, delete
    url(r'^new$', AppointmentCreateView.as_view(), name='new_appointment'),
    url(r'^(?P<pk>[0-9]+)/edit$',
            AppointmentUpdateView.as_view(),
            name='edit_appointment'),
    url(r'^(?P<pk>[0-9]+)/delete$',
            AppointmentDeleteView.as_view(),
            name='delete_appointment'),

]
