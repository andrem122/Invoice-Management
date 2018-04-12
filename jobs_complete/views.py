from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import user_passes_test
from customer_register.customer import Customer
from project_management.decorators import customer_and_staff_check
import csv

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def customer(request):
    current_user = request.user
    customer = Customer(current_user)

    houses = customer.completed_houses
    completed_jobs = customer.completed_jobs()

    #forms
    payment_history_form = Payment_History_Form()
    template = loader.get_template('jobs_complete/customer.html')

    context = {
        'houses': houses,
        'completed_jobs': completed_jobs,
        'current_user': current_user,
        'payment_history_form': payment_history_form,
    }

    return HttpResponse(template.render(context, request))
