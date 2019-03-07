from .utils import send_sms
from django.contrib.auth.models import User
from customer_register.customer import Customer
from project_details.house import _House

def format_message(address, percent):
    return '{address} is over {percent} percent of its budget.'.format(address=address, percent=percent)

def sms_budget_alerts():
    #send message to each customer
    customers = User.objects.filter(groups__name__in=['Customers'])

    #loop through customers
    for customer in customers:
        #get customer object
        _customer = Customer(customer)
        phone_number = customer.customer_user.phone_number

        #loop through customer houses
        for house in _customer.houses:
            #find out if budget is over 50%, 75%, 90%, and over budget
            budget_used = _House(house).budget_used()
            if budget_used > 50 and budget_used < 75:
                message = format_message(house.address, 50)
                send_sms(to=phone_number, message=message)
            elif budget_used > 75 and budget_used < 90:
                message = format_message(house.address, 75)
                send_sms(to=phone_number, message=message)
            elif budget_used > 90 and budget_used < 100:
                message = format_message(house.address, 90)
                send_sms(to=phone_number, message=message)
            else:
                message = '{address} is over budget!'
                send_sms(to=phone_number, message=message)
