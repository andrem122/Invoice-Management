from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import user_passes_test
from customer_register.customer import Customer
from send_data.forms import Send_Data
from project_management.decorators import customer_and_staff_check

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def customer(request):
    current_user = request.user
    customer = Customer(current_user)

    houses = customer.completed_houses()
    completed_jobs = customer.completed_jobs()

    #forms and templates
    payment_history_form = Payment_History_Form()
    send_data_form = Send_Data()
    template = loader.get_template('jobs_complete/customer.html')

    context = {
        'houses': houses,
        'completed_jobs': completed_jobs,
        'current_user': current_user,
        'payment_history_form': payment_history_form,
        'send_data_form': send_data_form,
    }

    return HttpResponse(template.render(context, request))
