from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from .forms import Approve_Job
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import login_required
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

        template = loader.get_template('jobs_admin/index.html')

        context = {
            'current_workers': current_workers,
            'jobs': jobs,
            'current_user': current_user,
            'payment_history_form': payment_history_form,
        }

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/accounts/login')

@login_required
def proposed_jobs(request):
    #get current user
    current_user = request.user
    if current_user.is_active and current_user.is_staff:

        #filter results by current week
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        #get all houses that have job proposals
        houses = House.objects.filter(proposed_jobs=True)

        #get all unapproved jobs for the current week
        jobs = Job.objects.filter(approved=False, start_date__range=[start_week, end_week])

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

                house = House.objects.filter(address=address)

                #update approved column to True for the specific job
                Job.objects.filter(id=job_id).update(approved=True)

                """add the user as a current worker on the house OR update current to True if they
                were a current worker OR do nothing if they are already active"""
                was_current = Current_Worker.objects.filter(house=house[0], company=current_user, current=False)
                is_current = Current_Worker.objects.filter(house=house[0], company=current_user, current=True)
                if was_current:
                    was_current[0].update(current=True)
                elif is_current:
                    pass
                else:
                    Current_Worker(house=house[0], company=current_user, current=True).save()

                """if there are no more unapproved jobs for a house,
                set proposed_jobs=False for that specific house
                """
                unapproved_jobs = Job.objects.filter(house=house[0], approved=False)

                if not unapproved_jobs:
                    House.objects.filter(address=address).update(proposed_jobs=False)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Approve_Job()

        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseRedirect('/accounts/login')
