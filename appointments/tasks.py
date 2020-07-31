import arrow, dramatiq, os
from django.conf import settings
from twilio.rest import Client
from django.template import loader
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
#from icalendar import Calendar, Event
from .models import Appointment_Base, Appointment_Medical, Appointment_Real_Estate


# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def generate_ics_file(appointment):
    """Generates an ics file"""
    pass
    # calendar = Calendar()
    # event = Event()
    #
    # summary = 'Appointment With {name}'.format(name=appointment.name)
    # appointment_time = arrow.get(appointment.time)
    #
    # event.add('summary', summary)
    # event.add('dtstart', )

def get_appointment_object(appointment_id, appointment_model):
    """Return an appointment object from any appointment model type"""

    model_to_query = Appointment_Base
    if appointment_model == 'Appointment_Medical':
        model_to_query = Appointment_Medical
    elif appointment_model == 'Appointment_Real_Estate':
        model_to_query = Appointment_Real_Estate

    try:
        # If appointment found, return appointment object
        appointment = model_to_query.objects.get(appointment_base_ptr_id=appointment_id)
        return appointment
    except model_to_query.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted or was never made, so we don't need to do anything
        return None

@dramatiq.actor
def send_new_appointment_notification(appointment_id, appointment_model):
    """Sends an html email and a text message to notify the client that an appointment has been made"""

    # Send a text and email to the company phone and email
    appointment = get_appointment_object(appointment_id, appointment_model)
    if appointment == None:
        # The appointment we were trying to remind someone about
        # has been deleted or was never made, so we don't need to do anything
        print('No appointment found')
        return

    # Variables for the email
    current_year = str(datetime.today().year)
    customer_type = appointment.company.customer_user.customer_type
    text_message = None
    context = None
    customer_user_first_name = appointment.company.customer_user.user.first_name
    additional_message = True

    # Appointment Details for base_appointment objects
    appointment_name = appointment.name
    appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone).format('MM/DD/YYYY hh:mm A')
    appointment_phone_number = appointment.phone_number.as_e164
    appointment_status = 'Yes' if appointment.confirmed == True else 'No'

    # End of notification text message
    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'alerts from NovaOne Software.'
    )

    if customer_type == 'MW':
        # Additional appointment details based on customer type
        print('MEDICAL WORKER')
        appointment_address = appointment.address
        appointment_city = appointment.city
        print(appointment_city)
        appointment_zip = appointment.zip
        appointment_email = appointment.email
        appointment_date_of_birth = appointment.date_of_birth
        appointment_gender = appointment.gender
        appointment_test_type = ', '.join(appointment.test_type)

        text_message = (
            'Hello {customer_user_first_name}, an appointment has been made. See details below:\n\n'
            'Name: {appointment_name}\n'
            'Appointment Time: {appointment_time}\n'
            'Phone Number: {appointment_phone_number}\n'
            'Patient Address: {appointment_address}\n'
            'City: {appointment_city}\n'
            'Zip: {appointment_zip}\n'
            'Email: {appointment_email}\n'
            'Date Of Birth: {appointment_date_of_birth}\n'
            'Gender: {appointment_gender}\n'
            'Test Type: {appointment_test_type}\n'
            'Confirmed: {appointment_status}\n'
            + end_of_reponse_message
            ).format(
                customer_user_first_name=customer_user_first_name,
                appointment_name=appointment_name,
                appointment_time=appointment_time,
                appointment_phone_number=appointment_phone_number,
                appointment_address=appointment_address,
                appointment_city=appointment_city,
                appointment_zip=appointment_zip,
                appointment_email=appointment_email,
                appointment_date_of_birth=appointment_date_of_birth,
                appointment_gender=appointment_gender,
                appointment_test_type=appointment_test_type,
                appointment_status=appointment_status,
            )
        print(text_message)

        context = {
                'customer_type': customer_type,
                'additional_message': additional_message,
                'customer_user_first_name': customer_user_first_name,
                'appointment_name': appointment_name,
                'appointment_time': appointment_time,
                'appointment_phone_number': appointment_phone_number,
                'appointment_address': appointment_address,
                'appointment_city': appointment_city,
                'appointment_zip': appointment_zip,
                'appointment_email': appointment_email,
                'appointment_date_of_birth': appointment_date_of_birth,
                'appointment_gender': appointment_gender,
                'appointment_test_type': appointment_test_type,
                'appointment_status': appointment_status,
                'current_year': current_year,
        }

    elif customer_type == 'PM':
        # Additional appointment details based on customer type
        appointment_unit_type = appointment.unit_type

        text_message = (
            'Hello, an appointment has been made. See details below:\n\n'
            'Name: {appointment_name}\n'
            'Appointment Time: {appointment_time}\n'
            'Phone Number: {appointment_phone_number}\n'
            'Unit Type: {appointment_unit_type}\n'
            'Confirmed: {appointment_status}'
            + end_of_reponse_message
            ).format(
                appointment_name=appointment_name,
                appointment_time=appointment_time,
                appointment_phone_number=appointment_phone_number,
                appointment_unit_type=appointment_unit_type,
                appointment_status=appointment_status,
            )

        context = {
                'customer_type': customer_type,
                'additional_message': additional_message,
                'customer_user_first_name': customer_user_first_name,
                'appointment_name': appointment_name,
                'appointment_time': appointment_time,
                'appointment_phone_number': appointment_phone_number,
                'appointment_unit_type': appointment_unit_type,
                'appointment_status': appointment_status,
                'current_year': current_year,
        }

    # Send text to the company number
    client.messages.create(
        body=text_message,
        to=appointment.company.phone_number.as_e164,
        from_=settings.TWILIO_NUMBER,
    )

    # Send a notification to me
    client.messages.create(
        body=text_message,
        to='+15613465571',
        from_=settings.TWILIO_NUMBER,
    )

    # Send email with html template
    path_to_template = os.path.join(settings.BASE_DIR, 'appointments', 'templates', 'appointments', 'new_appointment.html')
    html_content = loader.render_to_string(
        path_to_template,
        context,
    )

    subject, from_email = 'New Appointment', 'no-reply@novaonesoftware.com'
    msg = EmailMultiAlternatives(subject, text_message, from_email, [appointment.company.email], ['andre@novaonesoftware.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    success_message = 'New appointment notification sent successfully to {email}!'.format(email=appointment.company.email)
    return success_message

@dramatiq.actor
def send_appointment_reminder(appointment_id, appointment_model):
    """Send an appointment reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    appointment = get_appointment_object(appointment_id, appointment_model)
    if appointment == None:
        # The appointment we were trying to remind someone about
        # has been deleted or was never made, so we don't need to do anything
        print('No appointment found')
        return

    customer_type = appointment.company.customer_user.customer_type
    company_name = appointment.company.name
    company_number = appointment.company.phone_number
    appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)

    message = (
    'Hello {name}! You have an appointment coming up at {time} with {company_name}. '
    'Please reply "y" to confirm your appointment or "c" to cancel. Your appointment will be canceled '
    'if no response is recieved.\n\n'
    'This is an automated message. Reply "STOP" to end SMS alerts from {company_name}.'
    ).format(
        name=appointment.name.strip().title(),
        time=appointment_time.format('MM/DD/YYYY hh:mm A'),
        company_name=company_name,
    )

    if customer_type == 'MW':
        message = (
        'Hello {name}! You have an appointment coming up at {time} with {company_name} '
        'for a {test_type} test. '
        'Please reply "y" to confirm your appointment or "c" to cancel. Your appointment will be canceled '
        'if no response is recieved.\n\n'
        'This is an automated message. Reply "STOP" to end SMS alerts from {company_name}.'
        ).format(
            name=appointment.name.strip().title(),
            company_name=company_name,
            test_type=appointment.test_type,
            time=appointment_time.format('MM/DD/YYYY hh:mm A'),
        )
    elif customer_type == 'PM':
        message = (
        'Hello {name}! You have an appointment coming up at {time} for a showing at '
        '{address}. '
        'Please reply "y" to confirm your appointment or "c" to cancel. Your appointment will be canceled '
        'if no response is recieved.\n\n'
        'This is an automated message. Reply "STOP" to end SMS alerts from {company_name}.'
        ).format(
            name=appointment.name.strip().title(),
            time=appointment_time.format('MM/DD/YYYY hh:mm A'),
            address=appointment.company.address,
            company_name=company_name,
        )

    client.messages.create(
        body=message,
        to=appointment.phone_number.as_e164,
        from_=settings.TWILIO_NUMBER,
    )

    # Send a notification to me
    client.messages.create(
        body=message,
        to='+15613465571',
        from_=settings.TWILIO_NUMBER,
    )

@dramatiq.actor
def send_application_reminder(appointment_id):
    """Send application link after appointment to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        appointment = Appointment_Base.objects.get(pk=appointment_id)
    except Appointment_Base.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    address = appointment.company.address
    company_name = appointment.company.name
    company_number = appointment.company.phone_number

    message = (
    'Hello again {name}! We hope you enjoyed your showing at {company_name}. '
    'If you would like to apply, you can do so through the following link below:\n\n'
    'https://rentapp.zipreports.com/apply/graystone/ \n\n'
    'If you have any questions, please call {company_number}. '
    'Thank you and have a great day!\n\n'
    'This is an automated message. Reply "STOP" to end SMS alerts from {company_name}.'
    ).format(
        name=appointment.name.strip().title(),
        company_number=company_number,
        company_name=company_name,
    )

    client.messages.create(
        body=message,
        to=appointment.phone_number.as_e164,
        from_=settings.TWILIO_NUMBER,
    )

    # Send a notification to me
    client.messages.create(
        body=message,
        to='+15613465571',
        from_=settings.TWILIO_NUMBER,
    )
