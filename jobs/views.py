from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import House, Job, Current_Worker, Request_Payment
from django.contrib.auth.models import User
from .forms import Request_Payment_Form
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import worker_check
from django.contrib import messages
import datetime
import pytz

@user_passes_test(worker_check, login_url='/accounts/login/')
def index(request):
    current_user = request.user

    #get all houses that the contractor is working on for the customer
    current_workers = Current_Worker.objects.filter(company=current_user, current=True)

    #get all jobs for ONLY the current user that are approved and have a balance > 0
    approved_jobs = Job.objects.filter(company=current_user, approved=True, balance_amount__gt=0)

    """Pending Jobs"""
    #get all houses that the contractor has pending jobs for
    customer_id = current_user.groups.values_list('name', flat=True)[1]
    if customer_id == 'Workers':
        customer_id = customer.groups.values_list('name', flat=True)[0]
    customer_id = int(customer_id)
    customer = User.objects.get(pk=customer_id)

    customer_proposed_job_houses = House.objects.filter(customer=customer, proposed_jobs=True)

    #dates for filtering of query results
    today = datetime.datetime.now() + datetime.timedelta(days=2)
    start_delta = datetime.timedelta(days=today.weekday()+4)
    start_week = today.replace(hour=17, minute=0, second=0) - start_delta #start week is at 5:00PM one week back

    utc = pytz.UTC
    start_week = start_week.replace(tzinfo=utc)
    today = today.replace(tzinfo=utc)

    #get all jobs for ONLY the current user that were submitted in the last week, are unapproved, and have a balance > 0
    unapproved_jobs = Job.objects.filter(company=current_user, approved=False, balance_amount__gt=0, start_date__range=[start_week, today])

    def generate_queryset(outer_queryset, inner_queryset):
        for o in outer_queryset:
            for i in inner_queryset:
                if getattr(o, 'address') == getattr(getattr(i, 'house'), 'address'):
                    yield o
                    break

    worker_proposed_job_houses = generate_queryset(outer_queryset=customer_proposed_job_houses, inner_queryset=unapproved_jobs)

    template = loader.get_template('jobs/index.html')
    form = Request_Payment_Form()

    context = {
        'current_workers': current_workers,
        'pending_job_houses': worker_proposed_job_houses,
        'approved_jobs': approved_jobs,
        'unapproved_jobs': unapproved_jobs,
        'current_user': current_user,
        'form': form,
    }

    #check if generator 'generate_queryset' will have results
    if unapproved_jobs:
        context['gen_has_results'] = True

    #check if the user is new to send a welcome message
    new_user = request.GET.get('new_user')

    if new_user:
        context['new_user'] = new_user

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Request_Payment_Form(request.POST)

        if form.is_valid():
            #get job ID from POST
            job_id = int(request.POST.get('job_id'))

            #clean the form data and store into variables
            job = Job.objects.filter(id=job_id)
            amount = form.cleaned_data['amount']

            """if the current company already has a pending request for payment for a job for a house,
            do NOT write to the Request_Payment table"""
            house = House.objects.filter(address=job[0].house.address)
            flags = [
                Request_Payment.objects.filter(job=job[0], house=house[0], amount=amount, approved=False),
                House.objects.filter(address=job[0].house.address, pending_payments=True)
            ]

            if not flags[0]:
                # create an instance of the Request_Payment Class and populate it with the form data and default values
                payment = Request_Payment(job=job[0], house=house[0], amount=amount, approved=False)
                payment.save()
            if not flags[1]:
                house.update(pending_payments=True)

            return redirect('/jobs/thank_you')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Request_Payment_Form()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('jobs/thank_you.html')
    return HttpResponse(template.render(request=request))

#redirect a user after successful login
def redirect_user(request):
    if request.user.groups.filter(name='Customers').exists(): #if the user is a customer
        return redirect('/jobs_admin/proposed_jobs')
    elif request.user.groups.filter(name='Customers Staff').exists(): #if the user is customer's staff
        return redirect('/payment_requests/approved_payments')
    elif request.user.is_superuser:
        return redirect('/admin')
    else:
        return redirect('/jobs')
