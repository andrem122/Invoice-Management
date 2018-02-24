from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import login_required
from customer_register.customer import Customer

@login_required
def index(request):
    current_user = request.user
    if current_user.is_active and current_user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        customer = Customer(current_user)
        customer = customer.is_customer_staff()

        houses = customer.completed_houses
        jobs = customer.completed_jobs()

        #forms
        payment_history_form = Payment_History_Form()

        template = loader.get_template('jobs_complete/index.html')

        context = {
            'houses': houses,
            'jobs': jobs,
            'current_user': current_user,
            'payment_history_form': payment_history_form,
        }

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/accounts/login')
