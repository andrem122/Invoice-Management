from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, Request_Payment, House
from .forms import Payment_History_Form, Upload_Document_Form
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import customer_and_staff_check
from django.contrib import messages

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def p_history_job(request):
    current_user = request.user
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

                #get the job and house address associated with the payment
                job = Job.objects.get(pk=job_id)
                address = str(request.POST.get('job_house'))

                #get all approved payments for the job
                payments = Request_Payment.objects.filter(job=job, approved=True)

                #add it to the context dict
                context['payments'] = payments
                context['job_id'] = job_id
                context['address'] = address

        #for upload document form
        elif request.POST.get('upload-document'):

            p_id = int(request.POST.get('p_id'))
            payment = Request_Payment.objects.get(pk=p_id)

            #put the instance you want to update when the form saves into the form object
            upload_document_form = Upload_Document_Form(data=request.FILES, instance=payment)

            if upload_document_form.is_valid():
                #get the form data
                document_link = upload_document_form.cleaned_data['document_link']

                #update the document_link for the specific payment instance
                upload_document_form.save()

                redirect_url = request.POST.get('thank_you', None)
                if redirect_url is not None:
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
