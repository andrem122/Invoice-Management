from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from jobs.models import Job, Current_Worker, House
from .forms import AddJob
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customer_register.customer import Customer
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import worker_check

@user_passes_test(worker_check, login_url='/accounts/login/')
def add_job(request):
    current_user = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddJob(data=request.POST, files=request.FILES, user=current_user)

        if form.is_valid():

            #clean the form data and store into variables
            #variables for the Job instance
            house = form.cleaned_data['house']
            start_amount = form.cleaned_data['start_amount']

            """if the house already has proposed jobs, do NOT write to the House table"""
            flags = [
                        House.objects.filter(address=house.address, proposed_jobs=True),
                    ]

            if not flags[0]:
                #the house now has a proposed job, so set proposed_jobs=True
                house = House.objects.get(address=house.address)
                house.proposed_jobs=True
                house.save(update_fields=['proposed_jobs'])

            #save the uploaded file and the job
            job = form.save(commit=False)
            job.company = current_user
            job.total_paid = 0.00
            job.approved = False
            job.balance_amount = job.balance
            job.save()

            messages.success(request, 'Thanks! Your job was submitted and is awaiting approval.')
            form = AddJob(user=current_user)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddJob(user=current_user)
        
    return render(request, 'addjob/addjob.html', {'form': form})
