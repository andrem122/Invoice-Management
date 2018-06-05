from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import House, Job, Request_Payment
from .forms import Request_Payment_Form
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import worker_check
from django.contrib import messages
from register.worker import Worker

@user_passes_test(worker_check, login_url='/accounts/login/')
def index(request):
    current_user = request.user

    worker = Worker(current_user)
    approved_houses = worker.approved_houses()
    approved_jobs = worker.approved_jobs()
    unapproved_jobs = worker.unapproved_jobs()
    unapproved_houses = worker.unapproved_houses()

    template = loader.get_template('jobs/index.html')
    form = Request_Payment_Form()

    context = {
        'approved_houses': approved_houses,
        'approved_jobs': approved_jobs,
        'unapproved_houses': unapproved_houses,
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
            job = Job.objects.get(pk=job_id)
            house = House.objects.get(pk=job.house.id)
            amount = form.cleaned_data['amount']

            """if the current company already has a pending request for payment for a job for a house,
            do NOT write to the Request_Payment table"""
            # create an instance of the Request_Payment Class and populate it with the form data and default values
            payment, created = Request_Payment.objects.get_or_create(
                job=job,
                house=house,
                amount=amount,
                approved=False,
                requested_by_worker=True,
            )
            if not House.objects.filter(pk=house.id, pending_payments=True).exists():
                house.pending_payments = True
                house.save(update_fields=['pending_payments'])


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
        return redirect('/jobs_admin/')
    elif request.user.groups.filter(name='Customers Staff').exists(): #if the user is customer's staff
        return redirect('/payment_requests/approved_payments')
    elif request.user.is_superuser:
        return redirect('/admin')
    else:
        return redirect('/jobs')
