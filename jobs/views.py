from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import House, Job, Current_Worker, Request_Payment
from django.contrib.auth.models import User
from .forms import Request_Payment_Form

def index(request):
    #get all houses that the contractor is working on
    current_user = request.user
    current_workers = Current_Worker.objects.filter(company_id=current_user.id, current=True)

    #get all jobs for ONLY the current user and make sure they are approved
    jobs = Job.objects.filter(company_id=current_user.id, approved=True)

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
            #variables for the Job instance
            job = Job.objects.filter(id=job_id)
            amount = form.cleaned_data['amount']

            """if the current company already has a pending request for payment for a job for a house,
            do NOT write to the Request_Payment table"""
            flag = Request_Payment.objects.filter(job=job[0], amount=amount, approved=False)

            if not flag:
                # create an instance of the Request_Payment Class and populate it with the form data and default values
                payment = Request_Payment(job=job[0], amount=amount, approved=False)
                payment.save()

            return redirect('/accounts/login')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Request_Payment_Form()

    return HttpResponse(template.render(context, request))

#redirect a user after successful login
def redirect_user(request):
    #if the user is a staff member, redirect them to the admin page after login
    if request.user.is_staff is True:
        return redirect('/jobs_admin')
    else:
        return redirect('/jobs')
