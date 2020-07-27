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
from .forms import get_create_form, AppointmentFormUpdate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import PermissionDenied
from .models import Appointment_Real_Estate, Appointment_Base, Appointment_Medical
from customer_register.models import Customer_User
from property.models import Company, Company_Disabled_Datetimes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import arrow, pytz

def dispatch(class_name, class_instance, request, *args, **kwargs):
    # Check if there is a GET variable if not redirect to the home page
    try:
        company_id = int(request.GET.get('c', None))
    except ValueError:
        # Customer id was empty in GET variable
        raise Http404('Company not found!')
    except TypeError:
        # No GET variables attached to url
        raise Http404('Invalid url!')

    # Get the company
    company = None
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        # Company id was in GET variable but NOT found in database
        raise Http404('Company not found!')

    customer_id = company.customer_user.id
    if not request.user.is_superuser: # Will raise 'User object has no customer_user object if superuser'
        if request.user.is_authenticated and request.user.customer_user.id != customer_id:
            # Do not allow the customer_user (if they are logged in) to make appointments for other customers calendars
            raise PermissionDenied('Request denied!')

    return super(class_name, class_instance).dispatch(request, args, kwargs)

class AppointmentListView(LoginRequiredMixin, ListView):
    """Shows users a list of appointments"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects displayed by user

        # Get all companies owned by the user
        companies = Company.objects.filter(customer_user=self.request.user.customer_user)
        return Appointment_Base.objects.filter(
            company__in=companies
        ).order_by('-time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_user = self.request.user.customer_user
        customer_type = customer_user.customer_type
        companies = Company.objects.filter(customer_user=customer_user)

        if customer_type == 'MW': # For medical field
            appointments_medical = Appointment_Medical.objects.filter(company__in=companies)
            context['fields'] = ('Name', 'Time', 'Phone Number', 'Address', 'Email', 'Date Of Birth', 'Gender', 'Test Type', 'Confirmed') # fields to show in table header
            context['object_list'] = appointments_medical

        elif customer_type == 'PM': # For real estate
            appointments_real_estate = Appointment_Real_Estate.objects.filter(company__in=companies)
            context['fields'] = ('Name', 'Time', 'Phone Number', 'Unit Type', 'Confirmed')
            context['object_list'] = appointments_real_estate

        context['customer_user'] = customer_user
        return context

class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment_Base

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = kwargs['object'].company
        customer_type = company.customer_user.customer_type

        if customer_type == 'MW': # For medical field
            appointment_medical = Appointment_Medical.objects.get(pk=kwargs['object'].pk)
            context['appointment_medical'] = appointment_medical

        elif customer_type == 'PM': # For real estate
            appointment_real_estate = Appointment_Real_Estate.objects.get(pk=kwargs['object'].pk)
            context['appointment_real_estate'] = appointment_real_estate

        context['company'] = company
        return context

    def dispatch(self, request, *args, **kwargs):
        return dispatch(AppointmentDetailView, self, request, args, kwargs)

class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    template_name = 'appointments/appointment_form.html'
    success_message = 'Appointment successfully created.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request # Pass request object to form when it is initialized
        return kwargs

    def form_valid(self, form):
        # Set customer_id and timezone when form has been validated
        company_id = self.request.GET.get('c', None)
        company = Company.objects.get(id=int(company_id))
        appointment = form.save(commit=False) # Call form.save(commit=False) to create an object 'in memory' and not in the database
        appointment.time.replace(tzinfo=pytz.timezone('US/Eastern'))
        appointment.company = company
        appointment.save()

        # Schedule reminder for appointment two hours before appointment time
        appointment_task_id = appointment.schedule_reminder('send_appointment_reminder', -120)
        appointment.appointment_task_id = appointment_task_id

        # Schedule a notification message when somebody makes an appointment
        message = appointment.schedule_new_appointment_created_notification()
        print(message)
        appointment.save()

        # Return a JSON response if it is a POST request from the app
        # Get post parameters from app
        app_authentication_username = self.request.POST.get('PHPAuthenticationUsername', None)
        app_authentication_password = self.request.POST.get('PHPAuthenticationPassword', None)
        if app_authentication_username != None and app_authentication_password != None:
            return JsonResponse(data={'successReason': 'Successfully added appointment'}, status=201)
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        # Making an appointment from the app
        # Get post parameters from app and return first error as JSON
        app_authentication_username = self.request.POST.get('PHPAuthenticationUsername', None)
        app_authentication_password = self.request.POST.get('PHPAuthenticationPassword', None)
        if app_authentication_username != None and app_authentication_password != None:
            for field, errors in form.errors.items():
                return JsonResponse(data={'reason': form.errors[field][0]}, status=400)
        else:
            # If making an appointment from the website
            return super().form_invalid(form)

    def get_form_class(self):
        """Get the form class and fields based on the customer type"""

        # Get customer from url
        company_id = self.request.GET.get('c', None)
        company = Company.objects.get(pk=int(company_id))
        customer_type = company.customer_user.customer_type

        model = Appointment_Base
        if customer_type == 'MW': # medical worker customers
            model = Appointment_Medical
            fields = ['time', 'name', 'phone_number', 'address', 'email', 'date_of_birth', 'gender', 'test_type']

        elif customer_type == 'PM':
            model = Appointment_Real_Estate
            fields = ['time', 'name', 'phone_number', 'unit_type']

        return get_create_form(model, fields)

    def get_context_data(self, **kwargs):
        from datetime import datetime

        company_id = self.request.GET.get('c', None)
        company = Company.objects.get(id=int(company_id))

        now = datetime.now()
        appointments = Appointment_Base.objects.filter(
            time__gte=now,
            company=company,
        )

        disabled_datetimes_objects = Company_Disabled_Datetimes.objects.filter(company=company)

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

        disabled_datetimes_list = []
        for count, disabled_datetime_object in enumerate(disabled_datetimes_objects):
            disabled_datetime_from = arrow.get(disabled_datetime_object.disabled_datetime_from)
            disabled_datetime_to = arrow.get(disabled_datetime_object.disabled_datetime_to)

            disabled_datetime_from_string = (
            disabled_datetime_from.shift(minutes=-1)
            .to(disabled_datetime_object.time_zone.zone)
            .format('MM/DD/YYYY hh:mm A')
            )

            disabled_datetime_to_string = (
            disabled_datetime_to.to(disabled_datetime_object.time_zone.zone)
            .format('MM/DD/YYYY hh:mm A')
            )


            disabled_slot = (disabled_datetime_from_string, disabled_datetime_to_string)
            disabled_datetimes_list.append(disabled_slot)

        context = super().get_context_data(**kwargs)
        context['appointments'] = appointments_list
        context['disabled_datetimes'] = disabled_datetimes_list
        context['company'] = company

        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return dispatch(AppointmentCreateView, self, request, args, kwargs)

class AppointmentUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment_Real_Estate
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
        context['company_name'] = customer_user.company.name
        context['company_address'] = customer_user.company.address
        context['company_phone_number'] = customer_user.company.phone_number
        context['company_email'] = customer_user.company.email
        context['days_of_the_week_enabled'] = customer_user.company.days_of_the_week_enabled
        context['hours_of_the_day_enabled'] = customer_user.company.hours_of_the_day_enabled

        return context

class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment_Base

    def get_success_url(self):
        """Redirect user on successful deletion based on whether the user is anonymous or authenticated"""

        # User is authenticated and is NOT a super user
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            return reverse_lazy('appointments:list_appointments')

        # User is anonymous
        appointment = Appointment_Base.objects.get(pk=self.kwargs['pk'])
        company_id = str(appointment.company.id)
        return reverse_lazy('appointments:new_appointment') + '?c=' + company_id


def send_notifications(appointment_object, company_name, phone_numbers, emails,):
    """Sends an sms and email notification once an appointment has been
    confirmed"""

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'alerts from NovaOne Software.'
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
        'Appointment Time: {time}\n'
        'Phone Number: {phone_number}\n'
        + end_of_reponse_message
        ).format(
            is_confirmed=is_confirmed,
            name=appointment_object.name,
            time=appointment_time.format('MM/DD/YYYY hh:mm A'),
            phone_number=appointment_object.phone_number.as_e164,
        )

    customer_type = appointment_object.company.customer_user.customer_type
    if customer_type == 'PM':
        message = (
            'Hello, an appointment has been {is_confirmed}. See details below:\n\n'
            'Name: {name}\n'
            'Appointment Time: {time}\n'
            'Phone Number: {phone_number}\n'
            'Unit Type: {unit_type}'
            + end_of_reponse_message
            ).format(
                is_confirmed=is_confirmed,
                name=appointment_object.name,
                time=appointment_time.format('MM/DD/YYYY hh:mm A'),
                phone_number=appointment_object.phone_number.as_e164,
                unit_type=appointment_object.unit_type,
            )

    elif customer_type == 'MW':
        message = (
            'Hello, an appointment has been {is_confirmed}. See details below:\n\n'
            'Name: {name}\n'
            'Appointment Time: {time}\n'
            'Phone Number: {phone_number}\n'
            'Patient Address: {address}\n'
            'Email: {email}\n'
            'Date Of Birth: {date_of_birth}\n'
            'Gender: {gender}\n'
            'Test Type: {test_type}'
            + end_of_reponse_message
            ).format(
                is_confirmed=is_confirmed,
                name=appointment_object.name,
                time=appointment_time.format('MM/DD/YYYY hh:mm A'),
                phone_number=appointment_object.phone_number.as_e164,
                address=appointment_object.address,
                email=appointment_object.email,
                date_of_birth=appointment_object.date_of_birth,
                gender=appointment_object.gender,
                test_type=appointment_object.test_type,
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

def generate_appointment_url(request, company):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'

    return protocol + request.get_host() + '/appointments/new?c=' + str(company.id)

@twilio_view
def incoming_sms(request):
    """Responds to incoming sms"""

    incoming_sms = request.POST.get('Body', None)
    incoming_sms_number = request.POST.get('From', None)
    r = MessagingResponse()

    # Get our most recent appointment from the database for the phone number from Appointment_Base
    appointment = Appointment_Base.objects.filter(phone_number=incoming_sms_number).last()
    company = None
    customer_type = None

    try:
        # Get appointment time, customer user, and customer type if appointment object found
        appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)
        company = appointment.company
        customer_type = company.customer_user.customer_type
    except AttributeError as e:
        # No appointment object found
        print(e)

    # Get appointment type based on customer type
    if customer_type == 'MW':
        appointment = Appointment_Medical.objects.filter(appointment_base_ptr_id=appointment.pk).last()
    elif customer_type == 'PM':
        appointment = Appointment_Real_Estate.objects.filter(appointment_base_ptr_id=appointment.pk).last()

    # Set property values for company object
    if appointment != None:
        numbers_to_notify = (company.phone_number,)
        emails_to_notify = (company.email,)
        appointment_link = generate_appointment_url(request, company)
        company_number = company.phone_number
        company_name = company.name

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
    if appointment == None and (incoming_sms.lower() == 'y' or incoming_sms.lower() == 'c'):
        response_message = (
        'No appointment was found for number {number}.'
        + end_of_reponse_message
        ).format(number=incoming_sms_number, )

    # Appointment object found and appointment confirmed
    elif appointment != None and incoming_sms.lower() == 'y':
        # If appointment has passed and user still confirms
        if appointment_time < arrow.utcnow():
            response_message = (
            'Your appointment has passed. If you would like to make '
            'another appointment, you can do so by going online at {appointment_link}.'
            + end_of_reponse_message
            ).format(appointment_link=appointment_link)
            r.message(response_message)
            return r

        # Appointment is still available and user confirms
        if customer_type == 'PM': # Property Managers
            address = company.address # Address of property
            response_message = (
            'Your appointment at {time} has been confirmed. '
            'The address of the appointment is {address}. '
            'If you have any questions, please call {company_number} '
            'Thanks and see you then!'
            + end_of_reponse_message
            ).format(
                name=appointment.name.strip().title(),
                time=appointment_time.format('MM/DD/YYYY hh:mm A'),
                address=address,
                company_number=company_number,
            )

        elif customer_type == 'MW': # Medical workers
            address = appointment.address # Address of patient
            response_message = (
            'Your appointment at {time} has been confirmed. '
            'We will arrive shortly at your address, {address}. '
            'If you have any questions, please call {company_number}. '
            'Thanks and see you then!'
            + end_of_reponse_message
            ).format(
                name=appointment.name.strip().title(),
                time=appointment_time.format('MM/DD/YYYY hh:mm A'),
                address=address,
                company_number=company_number,
            )

        # Send notifications if appointment was not confirmed before
        if appointment.confirmed != True:
            send_notifications(appointment, company_name, numbers_to_notify, emails_to_notify)


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
            send_notifications(appointment, company_name, numbers_to_notify, emails_to_notify)

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
