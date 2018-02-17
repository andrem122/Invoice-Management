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

        #get all houses
        houses = House.objects.all()
        jobs = Job.objects.filter(approved=False)

        """check if houses have proposed jobs in the current week.
        if not, set proposed_jobs=False"""
        for h in houses.iterator():
            for j in jobs.iterator():
                if j.house == h:
                    proposed_jobs_for_house = Job.objects.filter(house=h, approved=False, start_date__range=[start_week, end_week])
                    if not proposed_jobs_for_house:
                        h.proposed_jobs=False
                        h.save(update_fields=['proposed_jobs'])
                    elif proposed_jobs_for_house:
                        h.proposed_jobs=True
                        h.save(update_fields=['proposed_jobs'])

        #get all houses with proposed jobs
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

                """If the house has no more proposed jobs for the current week,
                set proposed_jobs=False"""
                jobs = Job.objects.filter(house=house[0], approved=False, start_date__range=[start_week, end_week])

                if not jobs:
                    h = House.objects.filter(address=address)[0]
                    h.proposed_jobs=False
                    h.save(update_fields=['proposed_jobs'])

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Approve_Job()

        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseRedirect('/accounts/login')
