from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Request_Payment, House
from .forms import Payment_History_Form, Upload_Document_Form
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from django.contrib import messages
from utils.utils import get_succeeded

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def p_history_job(request, job_id):
    current_user = request.user
    template = loader.get_template('payment_history/p_history_job.html')
    upload_document_form = Upload_Document_Form()
    send_data_from = Send_Data()

    context = {
        'current_user': current_user,
        'upload_document_form': upload_document_form,
        'send_data_from': send_data_from,
    }

    #get the job and house address associated with the payment
    if get_succeeded(Job, pk=job_id):
        job = Job.objects.get(pk=job_id)
        address = job.house.address

        #get all payments for the job
        payments = Request_Payment.objects.filter(job=job)

        #add to context dict
        context['items'] = payments
        context['job_id'] = job_id
        context['address'] = address

    #form logic
    if request.method == 'POST':
        #for upload document form
        if request.POST.get('upload-document'):

            p_id = int(request.POST.get('p_id'))
            payment = Request_Payment.objects.get(pk=p_id)

            #put the instance you want to update when the form saves into the form object
            upload_document_form = Upload_Document_Form(request.POST, request.FILES, instance=payment)

            if upload_document_form.is_valid():

                #update the document_link for the specific payment instance
                upload_document_form.save()

                redirect_url = request.POST.get('thank_you', None)
                if redirect_url != None:
                    return redirect(redirect_url)
                else:
                    return redirect('/payment_history/thank_you')
    # if a GET (or any other method) we'll create a blank form
    else:
        upload_document_form = Upload_Document_Form()
        form = Payment_History_Form()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('payment_history/thank_you.html')
    return HttpResponse(template.render(request=request))
