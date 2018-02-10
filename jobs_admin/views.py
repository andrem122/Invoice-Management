from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from .forms import Approve_Job

def index(request):
    #get all houses that currently have workers working on them
    current_user = request.user
    sql = 'SELECT * FROM jobs_current_worker WHERE current=1 GROUP BY house_id'
    current_workers = Current_Worker.objects.raw(sql)

    #get all approved jobs
    jobs = Job.objects.filter(approved=True)

    template = loader.get_template('jobs_admin/index.html')

    context = {
        'current_workers': current_workers,
        'jobs': jobs,
        'current_user': current_user,
    }

    return HttpResponse(template.render(context, request))

def proposed_jobs(request):
    current_user = request.user

    #get all houses that have job proposals
    houses = House.objects.filter(proposed_jobs=True)

    #get all unapproved jobs
    jobs = Job.objects.filter(approved=False)

    #get form
    form = Approve_Job()

    template = loader.get_template('jobs_admin/proposed_jobs.html')

    context = {
        'houses': houses,
        'jobs': jobs,
        'current_user': current_user,
        'form': form
    }

    #form logic
    if request.method == 'POST':
        #get empty form
        form = Approve_Job(request.POST)

        if form.is_valid():
            #get job ID from POST
            job_id = int(request.POST.get('job_id'))
            address = str(request.POST.get('job_house'))

            #update approved column to True for the specific job
            Job.objects.filter(id=job_id).update(approved=True)

            """if there are no more unapproved jobs for a house,
            set proposed_jobs=False for that specific house
            """
            house = House.objects.filter(address=address)
            unapproved_jobs = Job.objects.filter(house=house[0], approved=False)

            if not unapproved_jobs:
                House.objects.filter(address=address).update(proposed_jobs=False)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Approve_Job()

    return HttpResponse(template.render(context, request))
