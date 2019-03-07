from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    """SMS utility method"""

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(body=message, to=to, from_='+15612202733')
    return response
