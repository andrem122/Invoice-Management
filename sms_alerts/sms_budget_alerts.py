from django.contrib.auth.models import User
from customer_register.customer import Customer
from project_details.house import _House
from twilio.rest import Client
from django.conf import settings
import datetime

def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)

def send_sms(to, message):
    """SMS utility method"""

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(body=message, to=to, from_=settings.TWILIO_NUMBER)
    return response

def format_message(address, percent, budget, total_spent):

    if percent >= 50:
        budget = as_currency(budget)
        total_spent = as_currency(total_spent)
        begin_message = 'WARNING: {percent}% of the budget for project {address} has been spent! Spend less money to ensure a profit.'.format(percent=percent, address=address)
        middle_message = '\n\nBudget: {budget}\nTotal Spent: {total_spent}'.format(budget=budget, total_spent=total_spent)
        end_message = '\n\nThis is an automated text message from Nova One Software Systems.'


        if percent >= 100:
            begin_message = 'WARNING: Project {address} is over budget!'.format(address=address)

        return begin_message + middle_message + end_message

    return None

def sms_budget_alerts():
    today = datetime.date.today()
    weekday = today.weekday()

    if (weekday == 5):
        #send message to each customer
        customers = User.objects.filter(groups__name__in=['Customers'], customer_user__wants_sms=True)

        #loop through customers
        for customer in customers:
            #get customer object
            _customer = Customer(customer)
            phone_number = customer.customer_user.phone_number.as_e164

            #loop through customer houses
            for house in _customer._houses(archived=False):
                #find out if budget is over 50%, 75%, 90%, and over budget
                _house = _House(house)
                percent_budget_used = _house.budget_used()
                budget = _house.budget()
                total_spent = _house.total_spent()

                message = format_message(house.address, percent_budget_used, budget, total_spent)

                if message != None:
                    send_sms(to=phone_number, message=message)
