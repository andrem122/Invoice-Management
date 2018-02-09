from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from jobs.models import Job, Current_Worker

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
