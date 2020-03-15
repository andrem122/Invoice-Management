import arrow, dramatiq
from django.conf import settings
from twilio.rest import Client
from .models import Appointment_Base, Appointment_Medical, Appointment_Real_Estate


# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

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
def send_appointment_reminder(appointment_id, appointment_model):
    """Send an appointment reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    appointment = get_appointment_object(appointment_id, appointment_model)
    if appointment == None:
        # The appointment we were trying to remind someone about
        # has been deleted or was never made, so we don't need to do anything
        print('No appointment found')
        return

    customer_type = appointment.customer_user.customer_type
    company_name = appointment.customer_user.company.name
    company_number = appointment.customer_user.company.phone_number
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
            address=appointment.customer_user.company.address,
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

    address = appointment.customer_user.company.address
    company_name = appointment.customer_user.company.name
    company_number = appointment.customer_user.company.phone_number

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
