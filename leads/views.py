from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from property.models import Company
from .models import Lead
from twilio.rest import Client
from django.conf import settings
from django.utils.timezone import now

def send_sms(to_number, from_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message,
        to=to_number,
        from_=from_number,
    )


@twilio_view
def incoming_call(request):
    """Responds to incoming calls on advertisements"""

    incoming_number = request.POST.get('From', None)
    twilio_number = request.POST.get('To', None)
    r = VoiceResponse()

    # Get the auto respond text for the number
    company = Company.objects.get(auto_respond_number=twilio_number)
    auto_respond_text = company.auto_respond_text

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'SMS alerts.'
    )

    # Create a lead object and save to database
    lead = Lead(
        name='From Sign',
        phone_number=incoming_number,
        email=None,
        renter_brand='From Sign',
        sent_text_date=now(),
        date_of_inquiry=now(),
        company=company,
    )
    lead.save()

    send_sms(incoming_number, twilio_number, auto_respond_text + end_of_reponse_message)

    r.say('Thanks for calling. We just sent you a text message with more information.')
    return r

@twilio_view
def incoming_sms(request):
    """Responds to incoming calls on advertisements"""

    incoming_number = request.POST.get('From', None)
    twilio_number = request.POST.get('To', None)
    r = MessagingResponse()

    # Get the auto respond text for the number
    company = Company.objects.get(auto_respond_number=twilio_number)
    auto_respond_text = company.auto_respond_text

    end_of_reponse_message = (
    '\n\nThis is an automated message. Reply "STOP" to end '
    'SMS alerts.'
    )

    # Create a lead object and save to database
    lead = Lead(
        name='From Sign',
        phone_number=incoming_number,
        email=None,
        renter_brand='From Sign',
        sent_text_date=now(),
        date_of_inquiry=now(),
        company=company,
    )
    lead.save()

    r.message(auto_respond_text + end_of_reponse_message)
    return r
