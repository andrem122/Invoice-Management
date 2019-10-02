from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
import arrow

from .models import Appointment


class AppointmentListView(ListView):
    """Shows users a list of appointments"""
    paginate_by = 25
    model = Appointment


class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment


class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'unit_type',]
    success_message = 'Appointment successfully created.'


class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'unit_type',]
    success_message = 'Appointment successfully updated.'


class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment
    success_url = reverse_lazy('appointments:list_appointments')

def send_confirmation_notification(appointment_object, apartment_complex_name, phone_numbers, emails):
    """Sends an sms and email notification once an appointment has been
    confirmed"""

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'alerts from {apartment_complex_name}.'.format(apartment_complex_name=apartment_complex_name)
    )
    appointment_time = arrow.get(appointment_object.time).to(appointment_object.time_zone.zone)

    # Setup message
    message = (
    'Hello, an appointment has been confirmed. See details below:\n'
    'Name: {name}\n'
    'Phone Number: {phone_number}\n'
    'Showing Time: {time}\n'
    'Unit Type: {unit_type}'
    + end_of_reponse_message
    ).format(
        name=appointment_object.name,
        phone_number=appointment_object.phone_number,
        time=appointment_time.format('h:mm a'),
        unit_type=appointment_object.unit_type,
    )

    # Send text notification
    for phone_number in phone_numbers:
        client.messages.create(
            body=message,
            to=phone_number,
            from_=settings.TWILIO_NUMBER,
        )

    # Send Email notification
    send_mail(
        'Appointment Confirmed',
        message,
        'no-reply@novaonesoftware.com',
        emails,
        fail_silently=False,
    )

@twilio_view
def incoming_sms(request):
    incoming_sms = request.POST.get('Body', None)
    incoming_sms_number = request.POST.get('From', None)
    address = '2929 Panthersville Rd, Decatur, GA 30034'
    apartment_complex_name = 'Hidden Villas Apartments'
    numbers_to_notify = ('+15613465571',)
    emails_to_notify = ['contact@mayfairatlawnwood.com', 'andre@graystonerealtyfl.com']
    r = MessagingResponse()

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'SMS alerts from {apartment_complex_name}.'.format(apartment_complex_name=apartment_complex_name)
    )

    response_message = (
    'Your response was not understood. Please reply "y" to '
    'confirm your appointment or "c" to cancel.'
    + end_of_reponse_message
    )

    # Get our most recent appointment from the database for the phone number
    appointment = Appointment.objects.filter(phone_number=incoming_sms_number).last()
    try:
        # Get appointment time if appointment object found
        appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)
    except AttributeError as e:
        # No appointment object found
        print(e)

    # Appointment object NOT found and reply is valid
    if appointment is None and (incoming_sms.lower() == 'y' or incoming_sms.lower() == 'c'):
        response_message = (
        'No appointment was found for number {number}. You can make an appointment '
        'online at https://www.novaonesoftware.com/appointments/new.'
        + end_of_reponse_message
        ).format(number=incoming_sms_number)

    # Appointment object found and appointment confirmed
    elif appointment is not None and incoming_sms.lower() == 'y':
        # If appointment has passed and user still confirms
        if appointment_time < arrow.utcnow():
            response_message = (
            'Your appointment has passed. If you would like to make '
            'another appointment, you can do so by going online at https://www.novaonesoftware.com/appointments/new.'
            + end_of_reponse_message
            )
            r.message(response_message)
            return r

        # Confirm appointment in database
        appointment.confirmed = True
        appointment.save()

        response_message = (
        'Your appointment at {time} has been confirmed. '
        'The address of the appointment is {address}. '
        'See you then!'
        + end_of_reponse_message
        ).format(
            name=appointment.name,
            time=appointment_time.format('h:mm a'),
            address=address,
        )

        # Send notifications
        #send_confirmation_notification(appointment, apartment_complex_name, numbers_to_notify, emails_to_notify)

    # Appointment object found and appointment canceled
    elif appointment is not None and incoming_sms.lower() == 'c':
        # If appointment has passed and user still confirms
        if appointment_time < arrow.utcnow():
            response_message = (
            'Your appointment has passed. If you would like to make '
            'another appointment, you can do so by going online at https://www.novaonesoftware.com/appointments/new.'
            + end_of_reponse_message
            )
            r.message(response_message)
            return r

        # Cancel appointment in database
        appointment.confirmed = False
        appointment.save()

        response_message = (
        'Your appointment has been canceled. If you would like to make '
        'another appointment, you can do so by going online at https://www.novaonesoftware.com/appointments/new.'
        + end_of_reponse_message
        )

    r.message(response_message)
    return r
