from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Request_Payment, House
from .forms import Payment_History_Form
from django.contrib.auth.decorators import login_required

@login_required
def p_history_job(request):
    #get the current user
    current_user = request.user
    if current_user.is_active and current_user.is_staff:

        template = loader.get_template('payment_history/p_history_job.html')

        context = {
            'current_user': current_user,
        }

        #form logic
        if request.method == 'POST':
            #get populated form
            payment_history_form = Payment_History_Form(request.POST)

            if payment_history_form.is_valid():
                #get job ID from POST
                job_id = int(request.POST.get('job_id'))

                #get the job associated with the payment
                job = Job.objects.filter(id=job_id)

                #get all approved payments for the job
                payments = Request_Payment.objects.filter(job=job[0], approved=True)

                #add it to the context dict
                context['payments'] = payments
                context['job_id'] = job_id

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Payment_History_Form()

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/accounts/login')
