from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from jobs.models import Job, Current_Worker, House
from .forms import AddJob
from django.contrib.auth.decorators import login_required

@login_required
def add_job(request):
    current_user = request.user

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddJob(request.POST, request.FILES)

        if form.is_valid():

            #clean the form data and store into variables
            #variables for the Job instance
            house = form.cleaned_data['house']
            start_amount = form.cleaned_data['start_amount']

            """if the current company already has been approved for a job for the house
            do NOT write to the Current_Worker table
            AND if the house already has proposed jobs, do NOT write to the House table"""
            flags = [
                        House.objects.filter(address=house.address, proposed_jobs=True),
                    ]

            if not flags[0]:
                #the house now has a proposed job, so set proposed_jobs=True
                House.objects.filter(address=house.address).update(proposed_jobs=True)

            #save the uploaded file and the job
            #job.generate_filename(request.FILES['document_link'].name)
            job = form.save(commit=False)
            job.company = current_user
            job.total_paid = 0.00
            job.approved = False
            job.balance_amount = job.balance
            job.save()

            return HttpResponseRedirect('/jobs')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddJob()

    return render(request, 'addjob/addjob.html', {'form': form})
