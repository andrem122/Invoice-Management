from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Request_Payment, House
from .forms import Payment_History_Form, Upload_Document_Form
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def p_history_job(request):
    current_user = request.user
    if current_user.is_active and current_user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        template = loader.get_template('payment_history/p_history_job.html')
        upload_document_form = Upload_Document_Form()

        context = {
            'current_user': current_user,
            'upload_document_form': upload_document_form,
        }

        #form logic
        if request.method == 'POST':
            #get job and payment ID from POST
            job_id = int(request.POST.get('job_id'))

            #for payment history form
            if request.POST.get('v-payment-history'):
                #get populated form
                payment_history_form = Payment_History_Form(request.POST)

                if payment_history_form.is_valid():

                    #get the job associated with the payment
                    job = Job.objects.get(pk=job_id)

                    #get all approved payments for the job
                    payments = Request_Payment.objects.filter(job=job, approved=True)

                    #add it to the context dict
                    context['payments'] = payments
                    context['job_id'] = job_id

            #for upload document form
            elif request.POST.get('upload-document'):

                p_id = int(request.POST.get('p_id'))
                payment = Request_Payment.objects.get(pk=p_id)

                #put the instance you want to update when the form saves into the form object
                upload_document_form = Upload_Document_Form(data=request.FILES, instance=payment)

                if upload_document_form.is_valid():
                    logger.error('Upload document form is valid!')
                    #get the form data
                    document_link = upload_document_form.cleaned_data['document_link']

                    #update the document_link for the specific payment instance
                    upload_document_form.save()

                    return redirect('/payment_history/thank_you')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = Payment_History_Form()
            upload_document_form = Upload_Document_Form()

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/accounts/login')

@login_required
def thank_you(request):
    template = loader.get_template('payment_history/thank_you.html')
    return HttpResponse(template.render(request=request))
