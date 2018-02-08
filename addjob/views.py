from django.shortcuts import render
from django.http import HttpResponseRedirect
from jobs.models import Job, Current_Worker

from .forms import AddJob

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
            company = current_user
            total_paid = 0.00
            approved = False
            document_link = 'http://andremashraghi.com'
            #variables for the Current Worker instance


            # create an instance of the Job and Current_Worker Class and populate it with the form data and default values
            job = Job(house=house, company=company, start_amount=start_amount, total_paid=total_paid, document_link=document_link, approved=approved)

            """if the current company already has been approved for a job in the house
            do NOT write to the Current_Worker table"""
            flag = Current_Worker.objects.filter(house=house, company=company, current=True)

            if not flag:
                current_worker = Current_Worker(house=house, company=company, current=False)
                current_worker.save()

            job.save()
            return HttpResponseRedirect('/jobs')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddJob()

    return render(request, 'addjob/addjob.html', {'form': form})
