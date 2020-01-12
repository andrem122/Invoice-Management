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
from django.shortcuts import redirect, get_object_or_404
import arrow, pytz, urllib.parse
from django.http import Http404
from django.core.exceptions import PermissionDenied

from .models import Appointment
from customer_register.models import Customer_User


class AppointmentListView(LoginRequiredMixin, ListView):
    """Shows users a list of appointments"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects displayed by user
        return Appointment.objects.filter(
            customer_user=self.request.user.customer_user
        ).order_by('-time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment

    def get_context_data(self, **kwargs):

        # Get customer by id
        customer_id = self.request.GET.get('c', None)
        customer = Customer_User.objects.get(id=int(customer_id))

        context = super().get_context_data(**kwargs)
        context['customer'] = customer
        return context

    def dispatch(self, request, *args, **kwargs):
        # Check if there is a GET variable if not redirect to the home page
        try:
            customer_id = int(request.GET.get('c', None))
        except ValueError:
            # Customer id was empty in GET variable
            raise Http404('Customer user not found!')
        except TypeError:
            # No GET variables attached to url
            raise Http404('Invalid url!')

        if request.user.is_authenticated and request.user.customer_user.id != customer_id:
            # Do not allow the customer_user (if they are logged in) to make appointments for other customers calendars
            raise PermissionDenied('Request denied!')

        try:
            customer_user = Customer_User.objects.get(id=customer_id)
        except Customer_User.DoesNotExist:
            # Customer id was in GET variable but NOT found in database
            raise Http404('Customer user not found!')

        return super().dispatch(request, *args, **kwargs)

class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    form_class = AppointmentFormCreate
    template_name = 'appointments/appointment_form.html'
    success_message = 'Appointment successfully created.'

    def get_context_data(self, **kwargs):
        from datetime import datetime

        customer_id = self.request.GET.get('c', None)
        customer_user = Customer_User.objects.get(id=int(customer_id))

        now = datetime.now()
        appointments = Appointment.objects.filter(
            time__gte=now,
            customer_user=customer_user,
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
        context['apartment_complex_name'] = customer_user.property.name
        context['apartment_complex_address'] = customer_user.property.address
        context['apartment_complex_phone_number'] = customer_user.property.phone_number
        context['apartment_complex_email'] = customer_user.property.email
        context['days_of_the_week_enabled'] = customer_user.property.days_of_the_week_enabled
        context['hours_of_the_day_enabled'] = customer_user.property.hours_of_the_day_enabled

        return context

    def form_valid(self, form):
        # Set customer_id and timezone when form has been validated
        customer_id = self.request.GET.get('c', None)
        customer_user = Customer_User.objects.get(id=int(customer_id))
        appointment = form.save(commit=False) # Call form.save(commit=False) to create an object 'in memory' and not in the database
        appointment.time.replace(tzinfo=pytz.timezone('US/Eastern'))
        appointment.customer_user = customer_user
        appointment.save()

        # Schedule reminder for appointment an hour before appointment time
        appointment_task_id = appointment.schedule_reminder('send_appointment_reminder', -60)
        appointment.appointment_task_id = appointment_task_id #
        appointment.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Check if there is a GET variable if not redirect to the home page
        try:
            customer_id = int(request.GET.get('c', None))
        except ValueError:
            # Customer id was empty in GET variable
            raise Http404('Customer user not found!')
        except TypeError:
            # No GET variables attached to url
            raise Http404('Invalid url!')

        if request.user.is_authenticated and request.user.customer_user.id != customer_id:
            # Do not allow the customer_user (if they are logged in) to make appointments for other customers calendars
            raise PermissionDenied('Request denied!')

        try:
            customer_user = Customer_User.objects.get(id=customer_id)
        except Customer_User.DoesNotExist:
            # Customer id was in GET variable but NOT found in database
            raise Http404('Customer user not found!')

        return super().dispatch(request, *args, **kwargs)

class AppointmentUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    form_class = AppointmentFormUpdate
    template_name = 'appointments/appointment_form.html'
    success_message = 'Appointment successfully updated.'

    def get_context_data(self, **kwargs):
        from datetime import datetime

        # Get single appointment by id
        appointment = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        customer_user = appointment.customer_user

        now = datetime.now()
        appointments = Appointment.objects.filter(
            time__gte=now,
            customer_user=customer_user,
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
        context['apartment_complex_name'] = customer_user.property.name
        context['apartment_complex_address'] = customer_user.property.address
        context['apartment_complex_phone_number'] = customer_user.property.phone_number
        context['apartment_complex_email'] = customer_user.property.email
        context['days_of_the_week_enabled'] = customer_user.property.days_of_the_week_enabled
        context['hours_of_the_day_enabled'] = customer_user.property.hours_of_the_day_enabled

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
        phone_number=appointment_object.phone_number.as_e164,
        time=appointment_time.format('MM/DD/YYYY hh:mm A'),
        unit_type=appointment_object.unit_type,
    )

    # Send text notification
    for phone_number in phone_numbers:
        client.messages.create(
            body=message,
            to=phone_number.as_e164,
            from_=settings.TWILIO_NUMBER,
        )

    # Send Email
    for email in emails:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
def generate_appointment_url(request, customer_user):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'

    return protocol + request.get_host() + '/appointments/new?c=' + str(customer_user.id)

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
        customer_user = appointment.customer_user
    except AttributeError as e:
        # No appointment object found
        print(e)

    # Set property values
    if appointment != None:
        address = customer_user.property.address
        numbers_to_notify = (customer_user.property.phone_number,)
        emails_to_notify = (customer_user.property.email,)
        appointment_link = generate_appointment_url(request, customer_user)
        apartment_complex_number = customer_user.property.phone_number
        apartment_complex_name = customer_user.property.name

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
