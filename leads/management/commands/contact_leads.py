from django.core.management.base import BaseCommand
import imaplib, phonenumbers
from bs4 import BeautifulSoup
from urllib import parse
from twilio.rest import Client
from itertools import chain
from datetime import datetime, timedelta
from django.conf import settings
from leads.models import Lead
from property.models import Company
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template import loader
from email import message_from_bytes
import os, pytz

class Command(BaseCommand):
    help = 'Contacts and collects leads from marketing campaigns via text message and email'

    def add_arguments(self, parser):
        parser.add_argument('--address', help='The company address', type=str, required=True)
        parser.add_argument('--company_name', help='The company name', type=str, required=True)
        parser.add_argument('--company_phone', help='The company phone number', type=str, required=True)
        parser.add_argument('--company_email', help='The company email', type=str, required=True)
        parser.add_argument('--company_id', help='The company id in the database property table', type=str, required=True)
        parser.add_argument('--notify_emails', help='The emails to notify', type=str, nargs='+', required=True)
        parser.add_argument('--emails_to_search', help='The emails to look for leads', type=str, required=True, nargs='+')
        parser.add_argument('--emails_to_search_pass', help='The emails to look for leads password', type=str, required=True, nargs='+')
        parser.add_argument('--emails_to_search_server', help='The emails to look for leads server name', type=str, required=True, nargs='+')
        parser.add_argument('--email_brands', help='The websites where lead emails are coming from', type=str, required=True, nargs='+')
        parser.add_argument('--form_link', help='The link to the pre-approval form', type=str, required=True)

    def handle(self, *args, **options):
        company_address = options['address']
        company_name = options['company_name']
        company_phone = options['company_phone']
        company_email = options['company_email']
        company_id = options['company_id']
        emails_to_notify = options['notify_emails']
        form_link = options['form_link']
        search_emails_info = zip(options['emails_to_search'], options['emails_to_search_pass'], options['emails_to_search_server'])
        email_brands = options['email_brands']

        self.main(
            search_emails_info,
            email_brands,
            company_address,
            company_name,
            company_phone,
            company_email,
            company_id,
            emails_to_notify,
            form_link,
        )

    def format_name(self, name):
        return name.strip().title()

    def get_current_year(self):
        return str(datetime.today().year)

    def format_date(self, date):
        index = date.find('+')

        if index == -1:
            index = date.find('-')

            if index == -1: #if the '-' is not found, simply return the date string
                return date

            return date[:index - 1]

        return date[:index - 1]

    def format_phone_number(self, phone):
        try:
            return phonenumbers.format_number(phonenumbers.parse(phone, 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
        except Exception as e:
            print('Could not format phone number!')
            return None

    def send_text(self, lead_info, company_address, company_phone, company_name, form_link):
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token  = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        first_name = lead_info['name'][0]
        full_name = ' '.join(lead_info['name'])
        unit_number = lead_info['unit_number'] if lead_info['unit_number'] != None else ''
        phone_number = self.format_phone_number(lead_info['phone'][0])

        text_message = (
        'Hello {name},\n\n'
        'We have received your inquiry about our apartment unit at {company_address}{unit_number}. '
        'Please fill out the quick, two minute form through the link below for consideration:\n\n'
        '{form_link}\n\n'
        'Please let us know if you have any questions by calling {company_phone}. Thanks!\n\n'
        'Regards,\n'
        '{company_name}\n\n'
        'This is an automated message.').format(
                                            name=first_name,
                                            company_address=company_address,
                                            unit_number=unit_number,
                                            form_link=form_link,
                                            company_phone=company_phone,
                                            company_name=company_name,
                                        )

        try:
            client.messages.create(
                to=phone_number,
                from_=settings.TWILIO_NUMBER,
                body=text_message
            )

            success_message = 'Text sent successfully to lead {full_name} !\n\n'.format(full_name=full_name) + text_message
            print(success_message)

            # Alter lead info dict if text is sent successfully
            lead_info['sent_text'] = True
            lead_info['sent_text_date'] = self.convert_to_utc(datetime.now())
            lead_info['sent_text_message'] = text_message
        except Exception as e:
            print(e)

    def send_email(self, lead_info, company_address, company_phone, company_name, company_email, form_link):
        first_name = lead_info['name'][0]
        unit_number = lead_info['unit_number'] if lead_info['unit_number'] != None else ''
        text_content = (
        'Hello {name},\n\n'
        'We have received your inquiry about our apartment unit at {company_address}{unit_number}. '
        'Please fill out the quick, two minute form through the link below for consideration:\n\n'
        '{form_link}\n\n'
        'Please let us know if you have any questions by calling {company_phone}. Thanks!\n\n'
        'Regards,\n'
        '{company_name}\n\n'
        'This is an automated message.').format(
                                            name=first_name,
                                            company_address=company_address,
                                            unit_number=unit_number,
                                            form_link=form_link,
                                            company_phone=company_phone,
                                            company_name=company_name,
                                        )

        subject = 'Thanks For Your Interest! - {company_name}'.format(company_name=company_name)
        email = EmailMessage(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [lead_info['lead_email']],
            reply_to=[company_email],
        )
        email.send()
        success_message = 'Email sent successfully to lead email {lead_email}!\n\n'.format(lead_email=lead_info['lead_email']) + text_content
        print(success_message)

        # Alter lead info dict if email is sent successfully
        lead_info['sent_email'] = True
        lead_info['sent_email_date'] = self.convert_to_utc(datetime.now())
        lead_info['sent_email_message'] = text_content


    def send_notification_email(self, lead_info, emails_to_notify, company_name):
        current_year = self.get_current_year()
        for email_to_notify in emails_to_notify:
            full_name = ' '.join(lead_info['name'])
            text_content = (
            'Inquiry about {company_name} recieved. See details below:\n\n'
            'Name: {name}\n'
            'Phone Number: {phone}\n'
            'Date of Inquiry: {date}\n'
            'Saw Listing On: {renter_brand}\n'
            'Email: {lead_email}\n'
            'Unit Number Interested In: {unit_number}\n\n'
            'A text message was sent to this lead. View what was sent below:\n\n'
            '{sent_text_message}\n\n'
            'An email was sent to this lead: View what was sent below:\n\n'
            '{sent_email_message}\n\n'
            'This is an automated message from Novaone.').format(
                       name=full_name,
                       company_name=company_name,
                       phone=lead_info['phone'][0],
                       date=self.date_to_string(lead_info['date_of_inquiry']),
                       renter_brand=lead_info['renterBrand'][0].title(),
                       lead_email=lead_info['lead_email'],
                       unit_number=lead_info['unit_number'],
                       sent_text_message=lead_info['sent_text_message'],
                       sent_email_message=lead_info['sent_email_message'],
                       )

            html_sent_text_message = lead_info['sent_text_message'].replace('\n', '<br />')
            html_sent_email_message = lead_info['sent_email_message'].replace('\n', '<br />')
            context = {
                    'name': full_name,
                    'phone': lead_info['phone'][0],
                    'lead_email': lead_info['lead_email'],
                    'date': self.date_to_string(lead_info['date_of_inquiry']),
                    'renter_brand': lead_info['renterBrand'][0].title(),
                    'sent_text_message': html_sent_text_message,
                    'sent_email_message': html_sent_email_message,
                    'current_year': current_year,
            }

            path_to_template = os.path.join(settings.BASE_DIR, 'leads', 'templates', 'leads', 'lead_contacted.html')
            html_content = loader.render_to_string(
                path_to_template,
                context,
            )

            subject, from_email = 'Lead Contacted!', 'no-reply@novaonesoftware.com'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to_notify])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            success_message = 'Notification email sent successfully to {email_to_notify}!'.format(email_to_notify=email_to_notify)
            print(success_message)

    def get_lead_info(self, mail_object, mail_id_list, email_brand):
        for mail_id in mail_id_list:
                typ, data = mail_object.fetch(mail_id, '(RFC822)')
                msg = message_from_bytes(data[0][1])
                date_of_inquiry = self.string_to_date(msg.get('date'))

                email_body = msg.get_payload(decode=True) # Very important to add decode=True
                if msg.is_multipart():
                    for payload in msg.get_payload():
                        email_body = payload.get_payload(decode=True)
                if email_brand == 'move':
                    yield self.parse_move_emails(email_body, date_of_inquiry)
                elif email_brand == 'zillow':
                    yield self.parse_zillow_emails(email_body, date_of_inquiry)
                elif email_brand == 'apartments':
                    yield self.parse_apartments_emails(email_body, date_of_inquiry)


    # Parsing Emails
    def parse_zillow_emails(self, email_body, date_of_inquiry):
        # Loop through anchor tags in html
        soup = BeautifulSoup(email_body, 'html.parser')
        items_to_remove = ['utm_medium', 'utm_campaign', 'utm_source', 'landlordBrand', 'inquiryId', 'intentionType', 'utm_term', 'controlHash']
        for tag in soup.findAll('a', href=True):
            if tag.text == 'phone contact info':
                parsed_url = parse.urlsplit(tag['href'])
                lead_info = parse.parse_qs(parsed_url.query)
                lead_info['date_of_inquiry'] = date_of_inquiry
                lead_info['lead_email'] = ''
                lead_info['renterBrand'][0] = lead_info['renterBrand'][0].title()
                lead_info['name'] = self.format_name(lead_info['name'][0]).split()
                lead_info['phone'] = [self.format_phone_number(lead_info['phone'][0])]
                lead_info['unit_number'] = ''
                lead_info['sent_email'] = False
                lead_info['sent_email_date'] = None
                lead_info['sent_email_message'] = 'No email message was sent to the lead because no email was provided.'
                lead_info['sent_text'] = False
                lead_info['sent_text_date'] = None
                lead_info['sent_text_message'] = 'No text message was sent to the lead because no phone number was provided.'
                lead_info['written_to_database'] = False

                # Remove items from dictionary we do not want
                for item in items_to_remove:
                    lead_info.pop(item)

                return lead_info

    def parse_move_emails(self, email_body, date_of_inquiry):
        soup = BeautifulSoup(email_body, 'html.parser')
        tags = soup.findAll('span')

        phone_number = self.format_phone_number(tags[8].text.strip())

        lead_info = {}
        lead_info['name'] = self.format_name(tags[6].text).split()
        lead_info['lead_email'] = tags[7].text.strip()
        lead_info['phone'] = [phone_number]
        lead_info['message'] = tags[10].text.strip()
        lead_info['unit_number'] = tags[3].text.strip().split('\r')[0][-3:] # Remove from dictionary from now for CSV writer
        lead_info['renterBrand'] = ['Realtor.com']
        lead_info['date_of_inquiry'] = date_of_inquiry
        lead_info['sent_email'] = False
        lead_info['sent_email_date'] = None
        lead_info['sent_email_message'] = 'No email message was sent to the lead because no email was provided.'
        lead_info['sent_text'] = False
        lead_info['sent_text_date'] = None
        lead_info['sent_text_message'] = 'No text message was sent to the lead because no phone number was provided.'
        lead_info['written_to_database'] = False

        return lead_info

    def parse_apartments_emails(self, email_body, date_of_inquiry):
        soup = BeautifulSoup(email_body, 'html.parser')
        tags = soup.findAll('a', href=True)

        lead_info = {}
        lead_info['lead_email'] = tags[3].text.strip()
        lead_info['renterBrand'] = ['Apartments.com']
        lead_info['unit_number'] = ''
        lead_info['sent_email'] = False
        lead_info['sent_email_date'] = None
        lead_info['sent_email_message'] = 'No email message was sent to the lead because no email was provided.'
        lead_info['sent_text'] = False
        lead_info['sent_text_date'] = None
        lead_info['sent_text_message'] = 'No text message was sent to the lead because no phone number was provided.'
        lead_info['written_to_database'] = False

        tags = soup.findAll('td')
        lead_info['name'] = self.format_name(tags[0].text).split()
        name_index  = tags[1].text.find('Name:')
        phone_index = tags[1].text.find('Phone:')

        if phone_index != -1:
            phone_info_list = tags[1].text[phone_index + 6: 400].strip().split('\n')
            phone_number = self.format_phone_number(phone_info_list[0])
            lead_info['phone'] = [phone_number]
        if name_index != -1:
            name_info_list = tags[1].text[name_index + 5: 600].replace('\r\n', '').strip().split()
            lead_info['name'] = [self.format_name(name_info_list[0]), self.format_name(name_info_list[1])]

        lead_info['date_of_inquiry'] = date_of_inquiry

        return lead_info


    def get_leads_from_email(self, imap_server, email, password, search_string):
        # Login to the email server via IMAP
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email, password)
        mail.select('inbox', readonly=True)
        mail.recent()
        status, data = mail.search(None, search_string)

        mail_ids = data[0]
        mail_id_list = mail_ids.split()
        return (mail, mail_id_list)

    def write_to_database(self, lead_info, company_id):
        name              = ' '.join(lead_info['name'])
        phone_number      = lead_info['phone'][0]
        email             = lead_info['lead_email']
        renter_brand      = lead_info['renterBrand'][0]
        date_of_inquiry   = lead_info['date_of_inquiry']
        sent_text_date    = lead_info['sent_text_date']
        sent_email_date   = lead_info['sent_email_date']
        company = Company.objects.get(pk=int(company_id))

        # Write to table
        lead = Lead(
            name=name,
            phone_number=phone_number,
            email=email,
            renter_brand=renter_brand,
            sent_text_date=sent_text_date,
            sent_email_date=sent_email_date,
            date_of_inquiry=date_of_inquiry,
            company=company,
        )
        lead.save()

        # Add 'written_to_database' key to lead_info dict with value of True after lead has been written to database
        lead_info['written_to_database'] = True


    def string_to_date(self, date_string):
        try:
            formatted_date_string = self.format_date(date_string)
            date = datetime.strptime(formatted_date_string, '%a, %d %b %Y %H:%M:%S')
            date = self.convert_to_utc(date)
            return date
        except ValueError as e:
            date = datetime.strptime(formatted_date_string, '%d %b %Y %H:%M:%S')
            date = self.convert_to_utc(date)
            return date
            print(e)

    def date_to_string(self, date_object):
        try:
            return date_object.strftime('%m/%d/%y %I:%M %p')
        except ValueError as e:
            print(e)
        except AttributeError as e:
            print(e)
            return date_object

    def convert_to_utc(self, date_object):
        """Converts a date object to UTC time zone"""
        utc = pytz.UTC
        try:
            converted_date = date_object.replace(tzinfo=utc)
            return converted_date
        except AttributeError:
            return date_object

    def convert_to_eastern(self, date_object):
        """Convert a date object to local time zone"""
        eastern = pytz.timezone('US/Eastern')
        try:
            converted_date = date_object.replace(tzinfo=eastern)
            return converted_date
        except AttributeError:
            return date_object

    def main(
        self,
        search_emails_info,
        email_brands,
        company_address,
        company_name,
        company_phone,
        company_email,
        company_id,
        emails_to_notify,
        form_link,):

        # Get date for emails sent up to a day ago
        utc = pytz.UTC
        date_now = datetime.now()
        date_one_day_ago = date_now - timedelta(days=4)
        sent_since_date = date_one_day_ago.strftime("%-d-%b-%Y")
        date_one_day_ago.replace(tzinfo=utc)

        for search_email, search_email_password, search_email_server in search_emails_info:
            """Search for leads in each email provided"""

            # Zillow, Trulia, Hotpads
            leads_info_1 = []
            if 'zillow' in email_brands:
                search_string = 'SENTSINCE {sent_since_date} (OR (OR (FROM "@convo.zillow.com") (FROM "@convo.trulia.com") ) (FROM "@convo.hotpads.com"))'.format(sent_since_date=sent_since_date)
                mail_object, mail_id_list = self.get_leads_from_email(search_email_server, search_email, search_email_password, search_string)
                leads_info_1 = self.get_lead_info(mail_object, mail_id_list, 'zillow')

            # Move.com
            leads_info_2 = []
            if 'move' in email_brands:
                search_string = 'SENTSINCE {sent_since_date} (FROM "RentalRequest@move.com")'.format(sent_since_date=sent_since_date)
                mail_object, mail_id_list = self.get_leads_from_email(search_email_server, search_email, search_email_password, search_string)
                leads_info_2 = self.get_lead_info(mail_object, mail_id_list, 'move')

            # Apartments.com
            leads_info_3 = []
            if 'apartments' in email_brands:
                search_string = 'SENTSINCE {sent_since_date} (FROM "lead@apartments.com")'.format(sent_since_date=sent_since_date)
                mail_object, mail_id_list = self.get_leads_from_email(search_email_server, search_email, search_email_password, search_string)
                leads_info_3 = self.get_lead_info(mail_object, mail_id_list, 'apartments')

            # Chain leads together from all websites
            leads_info = chain(leads_info_1, leads_info_2, leads_info_3)

            for lead_info in leads_info:

                #  Get lead info
                lead_phone_number = lead_info['phone'][0]
                lead_email        = lead_info['lead_email']
                name              = ' '.join(lead_info['name'])
                date_of_inquiry   = lead_info['date_of_inquiry']

                # Search through lead database for the phone number/email
                lead_found = None
                if lead_email != '': # If email exists, look for the lead by email in database
                    lead_found = Lead.objects.filter(email=lead_email).last()
                else: # if email does not exist for lead, then they must have a phone number, so look for that in the database
                    lead_found = Lead.objects.filter(phone_number=lead_phone_number).last()


                if lead_found != None: # Lead has been found in database
                    print("Lead {name} found in database!".format(name=lead_found.name))
                    # Contact leads who have contacted us again if they inquire again after 5 or more days since the bot has contacted them

                    # Convert all datetime objects to eastern time for comparison
                    date_of_inquiry = self.convert_to_eastern(date_of_inquiry)
                    date_one_day_ago = self.convert_to_eastern(date_one_day_ago)
                    sent_text_date = self.convert_to_eastern(lead_found.sent_text_date)
                    sent_email_date = self.convert_to_eastern(lead_found.sent_email_date)

                    # Contact leads by text
                    try:
                        if date_of_inquiry > date_one_day_ago and sent_text_date <= date_one_day_ago and lead_phone_number != None:
                            print('Lead {name} has contacted you again. Sending a text message...'.format(name=name))
                            self.send_text(lead_info, company_address, company_phone, company_name, form_link)
                    except TypeError:
                        pass # sent_text_date is NULL/None so we cannot compare it to a date object

                    # Contact leads by email
                    try:
                        if date_of_inquiry > date_one_day_ago and sent_email_date <= date_one_day_ago and lead_email != '':
                            print('Lead {name} has contacted you again. Sending an email message...'.format(name=name))
                            self.send_email(lead_info, company_address, company_phone, company_name, company_email, form_link)
                    except TypeError:
                        pass # sent_email_date is NULL/None so we cannot compare it to a date object

                    # Send notification emails and write to database
                    if lead_info['sent_text'] != False or lead_info['sent_email'] != False:
                        self.send_notification_email(lead_info, emails_to_notify, company_name)
                        self.write_to_database(lead_info, company_id)

                else: # Lead not found in database, so this code will run
                    print("Lead {name} not found in database!".format(name=name))
                    if lead_phone_number != None:
                        # Send text
                        self.send_text(lead_info, company_address, company_phone, company_name, form_link)

                    # Send email if lead email exists and is NOT found in database
                    if lead_email != '':
                        self.send_email(lead_info, company_address, company_phone, company_name, company_email, form_link)

                    # Phone NOT found in database and phone exists so write to database
                    if lead_phone_number != None:
                        self.write_to_database(lead_info, company_id)

                    # Email NOT found in database and email exists so write to database if it has not been written already
                    if lead_email != '' and lead_info['written_to_database'] == False:
                        self.write_to_database(lead_info, company_id)

                    # Send notification email if a text message or email was sent to the lead
                    if lead_info['sent_text'] != False or lead_info['sent_email'] != False:
                        self.send_notification_email(lead_info, emails_to_notify, company_name)
