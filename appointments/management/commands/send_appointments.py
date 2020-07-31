from django.core.management.base import BaseCommand, CommandError
from customer_register.models import Customer_User
from property.models import Company
from appointments.models import Appointment_Base, Appointment_Medical, Appointment_Real_Estate
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.http import HttpResponse
import os, csv, arrow
from io import StringIO

class Command(BaseCommand):
    help = 'Sends all appointments for each user in a CSV file'

    def create_csv(self, headers, appointments, customer_type):
        """Creates a CSV file"""

        csv_file = StringIO()
        writer = csv.writer(csv_file)

        for count, appointment in enumerate(appointments):

            if count == 0:
                # Write the headers to the csv on the first loop
                writer.writerow(headers)

            # Write data to csv file
            appointment_time = arrow.get(appointment.time).to(appointment.time_zone.zone)
            if customer_type == 'MW':
                writer.writerow((appointment.name, appointment_time.format('MM/DD/YYYY hh:mm A'), appointment.phone_number, appointment.address, appointment.city, appointment.zip, appointment.email, appointment.date_of_birth, appointment.gender, appointment.test_type, appointment.confirmed))
            elif customer_type == 'PM':
                writer.writerow((appointment.name, appointment_time.format('MM/DD/YYYY hh:mm A'), appointment.phone_number, appointment.unit_type, appointment.confirmed))

        return csv_file.getvalue() # return the csv as a file


    def send_email(self, customer_user):
        """Send an HTML email with the CSV file"""
        current_year = str(datetime.today().year)

        text_content = (
        'Hello {first_name}! Here is a CSV file with your appointments for the day.\n'
        'Thanks for being a customer, and have a great day!\n\n'
        'NovaOne Software\n'
        '(561) 346-5571'
        'andre@novaonesoftware.com'
        ).format(first_name=customer_user.user.first_name)

        context = {
                'first_name': customer_user.user.first_name,
                'current_year': current_year,
        }

        path_to_template = os.path.join(settings.BASE_DIR, 'appointments', 'templates', 'appointments', 'daily_appointments_notification.html')
        html_content = loader.render_to_string(
            path_to_template,
            context,
        )

        # Get all companies of the user to get all appointments
        customer_type = customer_user.customer_type
        companies = Company.objects.filter(customer_user=customer_user)
        now = datetime.now()

        appointments = None
        headers = None
        if customer_type == 'MW': # For medical field
            appointments = Appointment_Medical.objects.filter(company__in=companies, time__date=datetime.date(now))
            headers = ('Name', 'Time', 'Phone Number', 'Address', 'City', 'Zip', 'Email', 'Date Of Birth', 'Gender', 'Test Type', 'Confirmed') # fields to show in table header
        elif customer_type == 'PM': # For real estate
            appointments = Appointment_Real_Estate.objects.filter(company__in=companies, time__date=datetime.date(now))
            headers = ('Name', 'Time', 'Phone Number', 'Unit Type', 'Confirmed')

        # Send the email ONLY if there are appointments for the day
        if appointments.exists():
            csv_file = self.create_csv(headers, appointments, customer_type)

            subject, from_email = 'Daily Appointments', 'no-reply@novaonesoftware.com'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [customer_user.user.email], ['andre@novaonesoftware.com'])
            msg.attach_alternative(html_content, "text/html")
            msg.attach('appointments.csv', csv_file, 'text/csv')
            msg.send()

            success_message = 'Daily appointments email sent successfully to {email}!'.format(email=customer_user.user.email)
            print(success_message)
        else:
            fail_message = 'No appointments for today, so no email will be sent to {email}'.format(email=customer_user.user.email)
            print(fail_message)
    def handle(self, *args, **options):
        # Get all with email notifications enabled
        customer_users = Customer_User.objects.filter(wants_email_notifications=True)

        # Send an email to each user with the CSV file of appointments
        for customer_user in customer_users:
            self.send_email(customer_user)
