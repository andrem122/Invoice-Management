from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from .forms import Change_Job_Status
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import login_required
from jobs.dates_and_times import Dates_And_Times
import datetime

@login_required
def index(request):
    current_user = request.user
    if current_user.is_active and current_user.is_staff:
        #get all houses with current workers
        sql = 'SELECT * FROM jobs_current_worker WHERE current=1 GROUP BY house_id'
        current_workers = Current_Worker.objects.raw(sql)

        #get all approved jobs
        jobs = Job.objects.filter(approved=True, balance_amount__gt=0)

        #get the empty forms
        payment_history_form = Payment_History_Form()
        change_job_status_form = Change_Job_Status()

        #load template
        template = loader.get_template('jobs_admin/index.html')

        context = {
            'current_workers': current_workers,
            'jobs': jobs,
            'current_user': current_user,
            'payment_history_form': payment_history_form,
            'change_job_status_form': change_job_status_form,
        }

        #form logic
        if request.method == 'POST':
            #get empty form
            form = Change_Job_Status(request.POST)

            if form.is_valid():
                #get job ID from POST
                job_id = int(request.POST.get('job_id'))
                address = str(request.POST.get('job_house'))

                house = House.objects.get(address=address)

                #update approved column to False for the specific job
                job = Job.objects.get(pk=job_id)
                job.approved=False
                job.save()

                """if no more current jobs for specific house, delete as current worker"""
                current_house_jobs = Job.objects.filter(company=job.company, approved=True, house=house)

                if not current_house_jobs:
                    Current_Worker.objects.filter(company=job.company, house=house).delete()


        # if a GET (or any other method) we'll create a blank form
        else:
            form = Change_Job_Status()

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/accounts/login')

@login_required
def proposed_jobs(request):
    #get current user
    current_user = request.user
    if current_user.is_active and current_user.is_staff:

        #filter data by current week
        jobs_datetime = Dates_And_Times(House.objects.all(), Job.objects.filter(approved=False), Job)
        jobs_datetime.current_week_results(update_field={'proposed_jobs': [True, False]}, approved=False, start_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

        #get all houses with proposed jobs and unapproved jobs
        houses = House.objects.filter(proposed_jobs=True)
        jobs = Job.objects.filter(approved=False, start_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

        #get form
        form = Change_Job_Status()

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
            form = Change_Job_Status(request.POST)

            if form.is_valid():
                #get job ID from POST
                job_id = int(request.POST.get('job_id'))
                address = str(request.POST.get('job_house'))

                house = House.objects.filter(address=address)

                #update approved column to True for the specific job
                job = Job.objects.get(pk=job_id)
                job.approved=True
                job.save()

                """add the user as a current worker on the house OR update current to True if they
                were a current worker OR do nothing if they are already active"""
                was_current = Current_Worker.objects.filter(house=house[0], company=job.company, current=False)
                is_current = Current_Worker.objects.filter(house=house[0], company=job.company, current=True)
                if was_current:
                    was_current[0].update(current=True)
                elif is_current:
                    pass
                else:
                    Current_Worker(house=house[0], company=job.company, current=True).save()

                """If the house has no more proposed jobs for the current week,
                set proposed_jobs=False"""
                jobs = Job.objects.filter(house=house[0], approved=False, start_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

                if not jobs:
                    h = House.objects.filter(address=address)[0]
                    h.proposed_jobs=False
                    h.save(update_fields=['proposed_jobs'])

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Change_Job_Status()

        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseRedirect('/accounts/login')
