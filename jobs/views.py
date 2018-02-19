from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import House, Job, Current_Worker, Request_Payment
from django.contrib.auth.models import User
from .forms import Request_Payment_Form
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    current_user = request.user

    if current_user.is_active and current_user.groups.filter(name='Contractors').exists():
        customer_houses = ''
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
    else:
        return redirect('/accounts/login')

@login_required
def thank_you(request):
    template = loader.get_template('jobs/thank_you.html')
    return HttpResponse(template.render(request=request))

#redirect a user after successful login
def redirect_user(request):
    #if the user is a Customer or Customer Staff, redirect them to the admin page after login
    if request.user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        return redirect('/jobs_admin')
    elif request.user.is_superuser:
        return redirect('/admin')
    else:
        return redirect('/jobs')
