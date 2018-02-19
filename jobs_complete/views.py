from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Current_Worker, House
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    current_user = request.user
    if current_user.is_active and current_user.is_staff:
        #get all houses with completed jobs
        houses = House.objects.filter(completed_jobs=True)

        #get all approved jobs with a balance less than or equal to zero; limit to 50 results
        jobs = Job.objects.filter(approved=True, balance_amount__lte=0)[:50]

        #get the empty forms
        payment_history_form = Payment_History_Form()

        template = loader.get_template('jobs_complete/index.html')

        context = {
            'houses': houses,
            'jobs': jobs,
            'current_user': current_user,
            'payment_history_form': payment_history_form,
        }

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/accounts/login')
