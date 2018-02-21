from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from .forms import Change_Job_Status
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from jobs.dates_and_times import Dates_And_Times
from customer_register.customer import Customer
import datetime

@login_required
def index(request):
    current_user = request.user
    if current_user.is_active and current_user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        #get all customer houses and houses with active jobs
        customer = Customer(customer=current_user)
        current_houses = customer.current_houses
        approved_jobs = customer.approved_jobs()

        #get the empty forms
        payment_history_form = Payment_History_Form()
        change_job_status_form = Change_Job_Status()

        #load template
        template = loader.get_template('jobs_admin/index.html')

        context = {
            'current_workers': current_houses,
            'jobs': approved_jobs,
            'current_user': current_user,
            'payment_history_form': payment_history_form,
            'change_job_status_form': change_job_status_form,
        }

        #get the register url if it exists
        register_url = request.GET.get('url', None)

        if register_url:
            context['register_url'] = register_url

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

                #redirect because Django does not get database results after form submit
                return redirect('/jobs_admin')


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
    if current_user.is_active and current_user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():

        #filter data by current week for customer
        jobs_datetime = Dates_And_Times(House.objects.filter(customer=current_user), Job.objects.filter(approved=False), Job)
        jobs_datetime.current_week_results(update_field={'proposed_jobs': [True, False]}, approved=False, start_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

        #get all houses with unapproved jobs for only the customers houses
        houses = House.objects.filter(customer=current_user, proposed_jobs=True)
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

                house = House.objects.get(address=address)
                job = Job.objects.get(pk=job_id)

                #update approved column to True for the specific job
                job.approved=True
                job.save()

                """add the user as a current worker on the house OR update current to True if they
                were a current worker OR do nothing if they are already active"""
                was_current = Current_Worker.objects.filter(house=house, company=job.company, current=False)
                is_current = Current_Worker.objects.filter(house=house, company=job.company, current=True)
                if was_current:
                    was_current[0].update(current=True)
                elif is_current:
                    pass
                else:
                    Current_Worker(house=house, company=job.company, current=True).save()

                """If the house has no more proposed jobs for the current week,
                set proposed_jobs=False"""
                jobs = Job.objects.filter(house=house, approved=False, start_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

                if not jobs:
                    house.proposed_jobs=False
                    house.save(update_fields=['proposed_jobs'])

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Change_Job_Status()

        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseRedirect('/accounts/login')
