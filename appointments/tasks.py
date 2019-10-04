import arrow
import dramatiq

from django.conf import settings
from twilio.rest import Client
from .models import Appointment


# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


@dramatiq.actor
def send_sms_reminder(appointment_id):
    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    address = '2929 Panthersville Rd, Decatur, GA 30034'
    apartment_complex_name = 'Hidden Villas Apartments'
    appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)

    message = (
    'Hello {name}! You have an appointment coming up at {time} to see an apartment unit at '
    '{address}. '
    'Please reply "y" to confirm your appointment or "c" to cancel.\n\n'
    'This is an automated message. Reply "STOP" to end SMS alerts from {apartment_complex_name}.'
    ).format(
        name=appointment.name.strip().title(),
        address=address,
        time=appointment_time.format('h:mm a'),
        apartment_complex_name=apartment_complex_name,
    )

    client.messages.create(
        body=message,
        to=appointment.phone_number.as_e164,
        from_=settings.TWILIO_NUMBER,
    )
