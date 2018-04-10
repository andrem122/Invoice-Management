from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import House, Job, Current_Worker, Request_Payment
from django.contrib.auth.models import User
from .forms import Request_Payment_Form
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import worker_check
from django.contrib import messages

@user_passes_test(worker_check, login_url='/accounts/login/')
def index(request):
    current_user = request.user
    #get all houses that the contractor is working on for the customer
    current_workers = Current_Worker.objects.filter(company=current_user, current=True)

    #get all jobs for ONLY the current user that are approved and have a balance > 0
    jobs = Job.objects.filter(company=current_user, approved=True, balance_amount__gt=0)

    template = loader.get_template('jobs/index.html')
    form = Request_Payment_Form()

    context = {
        'current_workers': current_workers,
        'jobs': jobs,
        'current_user': current_user,
        'form': form,
    }

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
