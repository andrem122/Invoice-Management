from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
from .forms import AppointmentFormCreate, AppointmentFormUpdate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import arrow, pytz, urllib.parse

from .models import Appointment


class AppointmentListView(LoginRequiredMixin, ListView):
    """Shows users a list of appointments"""
    paginate_by = 25
    model = Appointment

class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment

    def get_context_data(self, **kwargs):
        apartment_complex_name = self.request.GET.get('apartment-complex-name', None)
        context = super().get_context_data(**kwargs)
        context['apartment_complex_name'] = apartment_complex_name
        return context

    def dispatch(self, request, *args, **kwargs):
        # Check if there is a GET variable if not redirect to the home page
        apartment_complex_name = request.GET.get('apartment-complex-name', None)
        if apartment_complex_name == None or apartment_complex_name == '':
            return redirect('/')
        else:
            return super().dispatch(request, *args, **kwargs)

class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    form_class = AppointmentFormCreate
    template_name = 'appointments/appointment_form.html'
    success_message = 'Appointment successfully created.'

    def get_context_data(self, **kwargs):
        from datetime import datetime

        apartment_complex_name = self.request.GET.get('apartment-complex-name', None)
        now = datetime.now()
        appointments = Appointment.objects.filter(
            time__gte=now,
            apartment_complex_name=apartment_complex_name
        )

        appointments_list = []
        for count, appointment in enumerate(appointments):
            appointment_time = arrow.get(appointment.time)

            start_appointment_time = (
            appointment_time.shift(minutes=-1)
            .to(appointment.time_zone.zone)
            .format('MM/DD/YYYY hh:mm A')
            )

            end_appointment_time = (
            appointment_time.shift(minutes=+29)
            .to(appointment.time_zone.zone)
            .format('MM/DD/YYYY hh:mm A')
            )


            appointment_slot = (start_appointment_time, end_appointment_time)

            appointments_list.append(appointment_slot)

        context = super().get_context_data(**kwargs)
        context['appointments'] = appointments_list

        if apartment_complex_name.lower() == 'hidden villas':
            context['apartment_complex_name'] = 'Hidden Villas Apartments'
            context['apartment_complex_address'] = '2929 Panthersville Rd, Decatur, GA 30034'
            context['apartment_complex_number'] = '786-818-3015'
            context['apartment_complex_email'] = 'jazmond@bluedrg.com'
        elif apartment_complex_name.lower() == 'mayfair at lawnwood':
            context['apartment_complex_name'] = 'Mayfair At Lawnwood'
            context['apartment_complex_address'] = '1800 Nebraska Avenue, Fort Pierce, FL 34950'
            context['apartment_complex_number'] = '772-242-3154'
            context['apartment_complex_email'] = 'contact@mayfairatlawnwood.com'

        return context

    def form_valid(self, form):
        # Set apartment_complex_name and timezone when form has been validated
        apartment_complex_name = self.request.GET.get('apartment-complex-name', None)
        appointment = form.save(commit=False) # Call form.save(commit=False) to create an object 'in memory' and not in the database
        appointment.apartment_complex_name = apartment_complex_name
        appointment.time.replace(tzinfo=pytz.timezone('US/Eastern'))
        appointment.save()

        # Schedule reminder for appointment an hour before appointment time
        appointment_task_id = appointment.schedule_reminder('send_appointment_reminder', -60)
        appointment.appointment_task_id = appointment_task_id #
        appointment.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Check if there is a GET variable if not redirect to the home page
        apartment_complex_name = request.GET.get('apartment-complex-name', None)
        if apartment_complex_name == None or apartment_complex_name == '':
            return redirect('/')
        else:
            return super().dispatch(request, *args, **kwargs)

class AppointmentUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    form_class = AppointmentFormUpdate
    template_name = 'appointments/appointment_form.html'
    success_message = 'Appointment successfully updated.'

    def get_context_data(self, **kwargs):
        from datetime import datetime

        now = datetime.now()
        appointments = Appointment.objects.filter(time__gte=now)

        appointments_list = []
        for count, appointment in enumerate(appointments):
            appointment_time = arrow.get(appointment.time)

            start_appointment_time = (
            appointment_time.shift(minutes=-1)
            .to(appointment.time_zone.zone)
            .format('MM/DD/YYYY hh:mm A')
            )

            end_appointment_time = (
            appointment_time.shift(minutes=+29)
            .to(appointment.time_zone.zone)
            .format('MM/DD/YYYY hh:mm A')
            )


            appointment_slot = (start_appointment_time, end_appointment_time)

            appointments_list.append(appointment_slot)

        context = super().get_context_data(**kwargs)
        context['appointments'] = appointments_list
        context['apartment_complex_name'] = 'Hidden Villas Apartments'
        context['apartment_complex_address'] = '2929 Panthersville Rd, Decatur, GA 30034'
        context['apartment_complex_number'] = '786-818-3015'
        context['apartment_complex_email'] = 'jazmond@bluedrg.com'
        return context


class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment
    success_url = reverse_lazy('appointments:list_appointments')

def send_notifications(appointment_object, apartment_complex_name, phone_numbers, emails,):
    """Sends an sms and email notification once an appointment has been
    confirmed"""

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'alerts from {apartment_complex_name}.'.format(apartment_complex_name=apartment_complex_name)
    )
    appointment_time = arrow.get(appointment_object.time).to(appointment_object.time_zone.zone)

    is_confirmed = 'confirmed'
    subject = 'Appointment Confirmed'
    if appointment_object.confirmed == True: # Appointment was canceled, but object not updated yet in database
        is_confirmed = 'canceled';
        subject = 'Appointment Canceled'

    message = (
    'Hello, an appointment has been {is_confirmed}. See details below:\n\n'
    'Name: {name}\n'
    'Phone Number: {phone_number}\n'
    'Showing Time: {time}\n'
    'Unit Type: {unit_type}'
    + end_of_reponse_message
    ).format(
        is_confirmed=is_confirmed,
        name=appointment_object.name,
        phone_number=appointment_object.phone_number,
        time=appointment_time.format('MM/DD/YYYY hh:mm A'),
        unit_type=appointment_object.unit_type,
    )

    # Send text notification
    for phone_number in phone_numbers:
        client.messages.create(
            body=message,
            to=phone_number,
            from_=settings.TWILIO_NUMBER,
        )

    # Send Email
    for email in emails:
        send_mail(
            subject,
            message,
            'no-reply@novaonesoftware.com',
            [email],
            fail_silently=False,
        )

@twilio_view
def incoming_sms(request):
    """Responds to incoming sms"""

    incoming_sms = request.POST.get('Body', None)
    incoming_sms_number = request.POST.get('From', None)
    r = MessagingResponse()

    # Get our most recent appointment from the database for the phone number
    appointment = Appointment.objects.filter(phone_number=incoming_sms_number).last()

    try:
        # Get appointment time if appointment object found
        appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)
        apartment_complex_name = appointment.apartment_complex_name
    except AttributeError as e:
        # No appointment object found
        print(e)

    # Set property values
    if appointment != None:
        if apartment_complex_name.lower() == 'hidden villas':
            get_parameter_value = urllib.parse.quote(apartment_complex_name)
            address = '2929 Panthersville Rd, Decatur, GA 30034'
            numbers_to_notify = ('+15613465571', '+17868183015')
            emails_to_notify = ('andre.mashraghi@gmail.com','rene@bluedrg.com', 'sabrina@bluedrg.com', 'terrell@bluedrg.com', 'jazmond@bluedrg.com')
            appointment_link = 'https://project-management-novaone.herokuapp.com/appointments/new?apartment-complex-name={get_parameter_value}'.format(get_parameter_value=get_parameter_value)
            apartment_complex_number = '(786) 818-3015'

        elif apartment_complex_name.lower() == 'mayfair at lawnwood':
            get_parameter_value = urllib.parse.quote(apartment_complex_name)
            address = '1800 Nebraska Avenue, Fort Pierce, FL 34950'
            numbers_to_notify = ('+17722423154', )
            emails_to_notify = ('contact@mayfairatlawnwood.com', )
            appointment_link = 'https://project-management-novaone.herokuapp.com/appointments/new?apartment-complex-name={get_parameter_value}'.format(get_parameter_value=get_parameter_value)
            apartment_complex_number = '(772) 242-3154'

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'SMS alerts.'
    )

    response_message = (
    'Your response was not understood. Please reply "y" to '
    'confirm your appointment or "c" to cancel.'
    + end_of_reponse_message
    )

    # Appointment object NOT found and reply is valid
    if appointment is None and (incoming_sms.lower() == 'y' or incoming_sms.lower() == 'c'):
        response_message = (
        'No appointment was found for number {number}.'
        + end_of_reponse_message
        ).format(number=incoming_sms_number, )

    # Appointment object found and appointment confirmed
    elif appointment is not None and incoming_sms.lower() == 'y':
        # If appointment has passed and user still confirms
        if appointment_time < arrow.utcnow():
            response_message = (
            'Your appointment has passed. If you would like to make '
            'another appointment, you can do so by going online at {appointment_link}.'
            + end_of_reponse_message
            ).format(appointment_link=appointment_link)
            r.message(response_message)
            return r

        response_message = (
        'Your appointment at {time} has been confirmed. '
        'The address of the appointment is {address}. '
        'If you have any questions, please call {apartment_complex_number} '
        'Thanks and see you then!'
        + end_of_reponse_message
        ).format(
            name=appointment.name.strip().title(),
            time=appointment_time.format('MM/DD/YYYY hh:mm A'),
            address=address,
            apartment_complex_number=apartment_complex_number,
        )

        # Send notifications if appointment was not confirmed before
        if appointment.confirmed != True:
            send_notifications(appointment, apartment_complex_name, numbers_to_notify, emails_to_notify)


        # Confirm appointment in database and schedule apply reminder
        # apply_task_id = appointment.schedule_reminder('send_application_reminder', +30)
        # appointment.apply_task_id = apply_task_id
        appointment.confirmed = True
        appointment.save()

    # Appointment object found and appointment canceled
    elif appointment is not None and incoming_sms.lower() == 'c':
        # If appointment has passed and user still confirms
        if appointment_time < arrow.utcnow():
            response_message = (
            'Your appointment has passed. If you would like to make '
            'another appointment, you can do so by going online at {appointment_link}.'
            + end_of_reponse_message
            ).format(appointment_link=appointment_link)
            r.message(response_message)
            return r

        # Send notifications if appointment was confirmed before
        if appointment.confirmed == True:
            send_notifications(appointment, apartment_complex_name, numbers_to_notify, emails_to_notify)

        # Cancel appointment in database
        appointment.confirmed = False
        appointment.save()

        response_message = (
        'Your appointment has been canceled. If you would like to make '
        'another appointment, you can do so by going online at {appointment_link}.'
        + end_of_reponse_message
        ).format(appointment_link=appointment_link)

    r.message(response_message)
    return r
