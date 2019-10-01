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

    appointment_time = arrow.get(appointment.time, appointment.time_zone.zone)
    message = (
    'Hello {name}! You have an appointment coming up at {time} to see an apartment unit at '
    '1800 Nebraska Avenue, Fort Pierce, FL 34950 '
    'Please reply "y" to confirm your appointment or "c" to cancel.\n\n'
    'This is an automated message Reply "STOP" to end SMS alerts from Mayfair At Lawnwood.'
    ).format(
        name=appointment.name,
        time=appointment_time.format('h:mm a'),
    )

    client.messages.create(
        body=body,
        to=appointment.phone_number,
        from_=settings.TWILIO_NUMBER,
    )
