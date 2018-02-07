from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import House, Job
from django.contrib.auth.models import User

def index(request):
    #get all houses that have a job with the current user
    current_user = request.user
    houses = House.objects.filter(contractors=current_user.id)

    #get all jobs for ONLY the current user
    jobs = Job.objects.filter(company_id=current_user.id)

    template = loader.get_template('jobs/index.html')
    context = {
        'houses': houses,
        'jobs': jobs,
        'current_user': current_user,
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

#redirect a user after successful login
def redirect_user(request):
    #if the user is a staff member, redirect them to the admin page after login
    if request.user.is_staff is True:
        return redirect('/admin')
    else:
        return redirect('/jobs')
