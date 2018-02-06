from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import House, Job

def index(request):
    #get all rows from the Jobs and House tables
    houses = House.objects.all()
    jobs = Job.objects.all()
    template = loader.get_template('jobs/index.html')
    context = {
        'houses': houses,
        'jobs': jobs,
    }
    return HttpResponse(template.render(context, request))

def job_detail(request, job_id):
    #get all rows from the Jobs and House tables
    houses = House.objects.all()
    jobs = Job.objects.all()
    template = loader.get_template('jobs/job_detail.html')
    context = {
        'houses': houses,
        'jobs': jobs,
    }
    return HttpResponse(template.render(context, request))
