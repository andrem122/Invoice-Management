import arrow, dramatiq
from django.conf import settings
from twilio.rest import Client
from .models import Appointment


# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@dramatiq.actor
def send_appointment_reminder(appointment_id):
    """Send an appointment reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted or was never made, so we don't need to do anything
        return

    address = appointment.customer_user.property.address
    apartment_complex_name = appointment.customer_user.property.name
    apartment_complex_number = appointment.customer_user.property.phone_number

    appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)

    message = (
    'Hello {name}! You have an appointment coming up at {time} to see an apartment unit at '
    '{address}. '
    'Please reply "y" to confirm your appointment or "c" to cancel. Your appointment will be canceled '
    'if no response is recieved.\n\n'
    'This is an automated message. Reply "STOP" to end SMS alerts from {apartment_complex_name}.'
    ).format(
        name=appointment.name.strip().title(),
        address=address,
        time=appointment_time.format('MM/DD/YYYY hh:mm A'),
        apartment_complex_name=apartment_complex_name,
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
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    address = appointment.customer_user.property.address
    apartment_complex_name = appointment.customer_user.property.name
    apartment_complex_number = appointment.customer_user.property.phone_number

    message = (
    'Hello again {name}! We hope you enjoyed your showing at {apartment_complex_name}. '
    'If you would like to apply, you can do so through the following link below:\n\n'
    'https://rentapp.zipreports.com/apply/graystone/ \n\n'
    'If you have any questions, please call {apartment_complex_number}. '
    'Thank you and have a great day!\n\n'
    'This is an automated message. Reply "STOP" to end SMS alerts from {apartment_complex_name}.'
    ).format(
        name=appointment.name.strip().title(),
        apartment_complex_number=apartment_complex_number,
        apartment_complex_name=apartment_complex_name,
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
