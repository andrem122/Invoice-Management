from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from jobs.models import Job, Request_Payment
from project_details.house import _House
from .forms import Approve_Job, Approve_As_Payment, Reject_Estimate, Edit_Job
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.core.mail import send_mail
from send_data.forms import Send_Data
from django.core.exceptions import ObjectDoesNotExist
from customer_register.customer import Customer
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from itertools import chain
from payment_history.forms import Upload_Document_Form
from expenses.forms import Delete_Expense
from search_submit.views import Search_Submit_View
from ajax.ajax import Ajax
from django.conf import settings

def send_approval_mail(request, job_object, subject, html_title):
    template_message = 'Your job at {} for ${} has been approved!'.format(job_object.house.address, job_object.start_amount)
    username = job_object.company.get_username()
    context = {
        'username': username,
        'template_message': template_message,
        'title': html_title,
        'host_url': request.build_absolute_uri('/'),
    }
    html_message = render_to_string('email/approved.html', context)
    plain_message = """Hi {},\n\nYour job at {} for ${} has been approved!\n\nThanks for your cooperation.\nNova One Software Systems\n\n**This is an automated message. Please do not reply**
    """.format(username, job_object.house.address, job_object.start_amount)
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [job_object.company.email],
        fail_silently=False,
        html_message=html_message,
    )

def load_ajax_search_results(request):
    """Loads ajax html for the search view"""
    search_submit_context = {
        'current_user': request.user,
        'query': request.POST.get('query', None),
        'post_from_url': request.POST.get('post_from_url', None),
        'edit_job_form': Edit_Job(user=request.user),
        'approve_form': Approve_Job(),
        'approve_as_payment_form': Approve_As_Payment(),
        'reject_estimate_form': Reject_Estimate(),
        'upload_document_form': Upload_Document_Form(),
        'delete_exp_form': Delete_Expense(),
    }

    search_submit_view = Search_Submit_View()
    html = search_submit_view.search_results(
        query=search_submit_context.get('query'),
        request=request,
        context=search_submit_context,
        ajax=True)

    return html

def approve_job(request, customer):
    """
    Called when a user approves a job
    """
    approve_form = Approve_Job(request.POST)
    if approve_form.is_valid():
        #get POST data
        job_id = int(request.POST.get('job_id'))
        post_from_url = request.POST.get('post_from_url', None)

        job = Job.objects.filter(pk=job_id).add_balance()[0]
        house = job.house

        #update approved column to True for the specific job
        job.approved = True
        job.rejected = False
        job.save(update_fields=['approved', 'rejected'])

        #send approval email
        send_approval_mail(request, job, 'Job Approved!', 'Job Approved!')

        if request.is_ajax():

            #return ajax results for the search query else return results for /jobs-admin/
            if 'search' in post_from_url:
                return load_ajax_search_results(request)
            else:
                ajax = Ajax(customer)
                html = ajax.load_ajax_results('jobs')
                return html

        else:
            return request.POST.get('post_from_url', None)

def approve_as_payment(request, customer):
    approve_as_payment_form = Approve_As_Payment(request.POST)
    if approve_as_payment_form.is_valid():
        #get POST data
        job_id = int(request.POST.get('job_id'))
        post_from_url = request.POST.get('post_from_url', None)

        #get the job and house
        job = Job.objects.get(pk=job_id)
        house = job.house

        #amount requested for payment of job
        amount = float(job.start_amount)

        #add payment object to database
        Request_Payment.objects.create(job=job, house=house, amount=amount, approved=True)

        #update total paid for job
        job.approved = True
        job.save(update_fields=['approved'])

        #send approval email to worker
        send_approval_mail(request, job, 'Payment Approved!', 'Payment Approved!')

        if request.is_ajax():
            if 'search' in post_from_url:
                return load_ajax_search_results(request)
            else:
                ajax = Ajax(customer)
                html = ajax.load_ajax_results('jobs')
                return html
        else:
            return request.POST.get('post_from_url', None)

def reject_estimate(request, customer):
    reject_estimate_form = Reject_Estimate(request.POST)
    if reject_estimate_form.is_valid():
        #get POST data
        job_id = int(request.POST.get('job_id'))
        post_from_url = request.POST.get('post_from_url', None)

        #get the job and house
        job = Job.objects.get(pk=job_id)
        house = job.house

        #set rejected equal to True for the estimate/job
        job.approved = False
        job.rejected = True

        #update job total paid and delete payment object if payment object associated with job was NOT requested by the worker
        try:
            payment = Request_Payment.objects.filter(job=job, requested_by_worker=False)
            payment.delete() #delete payments generated by system
        except IndexError as e:
            print('No elements in the "Request_Payment" QuerySet, so an IndexError will occur')

        job.save()

        if request.is_ajax():
            if 'search' in post_from_url:
                return load_ajax_search_results(request)
            else:
                ajax = Ajax(customer)
                html = ajax.load_ajax_results('jobs')
                return html
        else:
            return request.POST.get('post_from_url', None)

def edit_job(request, customer):
    """
    Called when a user edits a job's properties
    """
    job_id = int(request.POST.get('job_id')) #get job id from POST request
    job = get_object_or_404(Job, id=job_id) #get job instance
    post_from_url = request.POST.get('post_from_url', None)

    edit_job_form = Edit_Job(data=request.POST, files=request.FILES, user=request.user)

    if edit_job_form.is_valid():

        previous_house = job.house #the house the job object belonged to before it is changed
        previous_company = job.company
        new_house = edit_job_form.cleaned_data.get('house', None)
        new_company = edit_job_form.cleaned_data.get('company', None)
        new_job_type = edit_job_form.cleaned_data.get('job_type', None)
        document_link = edit_job_form.cleaned_data.get('document_link', None)
        notes = edit_job_form.cleaned_data.get('notes', None)
        start_amount = edit_job_form.cleaned_data.get('start_amount', None)

        #update the job instance based on which fields were submitted in the form
        if new_house != None and new_house != previous_house:
            job.house = new_house

            #update objects
            Request_Payment.objects.filter(job__pk=job_id).update(house=new_house) #get payments associated with job instance
            job.save(update_fields=['house'])

        if new_company != None and new_company != previous_company:
            job.company = new_company
            job.save(update_fields=['company'])

        if new_job_type != None:
            #change and save new job type on job object
            job.job_type = new_job_type
            job.save(update_fields=['job_type'])

        if document_link != None:
            job.document_link = document_link
            job.save(update_fields=['document_link'])

        if notes != None:
            job.notes = notes
            job.save(update_fields=['notes'])

        if start_amount != None and 1 + float(start_amount) != 1.0: #update balance_amount if start_amount is in the POST data
            job.start_amount = start_amount
            job.balance_amount = job.balance
            job.save(update_fields=['start_amount', 'balance_amount'])

    else:
        print(edit_job_form.errors)


    if request.is_ajax():
        if 'search' in post_from_url:
            return load_ajax_search_results(request)
        else:
            ajax = Ajax(customer)
            html = ajax.load_ajax_results('jobs')
            return html
    else:
        return request.POST.get('post_from_url', None)

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def index(request):
    #get current user
    customer = Customer(request.user)

    #get active houses and houses with estimates
    active_houses = customer.active_houses()
    estimate_houses = customer.current_week_proposed_jobs_houses()
    completed_houses = customer.current_week_completed_houses()
    rejected_houses = customer.current_week_rejected_job_houses()

    #get estimates, approved, completed, and rejected jobs
    estimates = customer.current_week_proposed_jobs().add_balance()
    approved_jobs = customer.approved_jobs()
    completed_jobs = customer.current_week_completed_jobs().add_balance()
    rejected_jobs = customer.current_week_rejected_jobs().add_balance()


    #combine querysets and keep unique values for houses
    houses = set(chain(active_houses, estimate_houses, completed_houses, rejected_houses))
    jobs = list(chain(estimates, approved_jobs, completed_jobs, rejected_jobs))

    start_week = str(Customer.start_week.date())
    today = str(Customer.today.date())

    #get forms and template
    approve_form = Approve_Job()
    approve_as_payment_form = Approve_As_Payment()
    reject_estimate_form = Reject_Estimate()
    edit_job_form = Edit_Job(user=request.user)
    send_data_form = Send_Data()
    template = loader.get_template('jobs_admin/jobs_admin.html')
    job_results = loader.get_template('jobs_admin/jobs_admin_results.html')
    post_from_url = request.build_absolute_uri()

    context = {
        'houses': houses,
        'items': jobs,
        'current_user': request.user,
        'approve_form': approve_form,
        'approve_as_payment_form': approve_as_payment_form,
        'reject_estimate_form': reject_estimate_form,
        'edit_job_form': edit_job_form,
        'send_data_form': send_data_form,
        'start_week': start_week,
        'today': today,
        'post_from_url': post_from_url,
    }

    #get the register urls if they exist
    worker_url = request.GET.get('worker_url', None)
    staff_url = request.GET.get('staff_url', None)

    if worker_url and staff_url:
        #replace '?' with '&' in staff_url
        index = staff_url.find('staff') - 1
        staff_url = staff_url[:index] + '&' + staff_url[index+1:]

        context['worker_url'] = worker_url
        context['staff_url'] = staff_url

    # HTTP requests
    if request.method == 'POST':
        response = '<h2>Error</h2>'

        if request.POST.get('approve_job'):
            response = approve_job(request, customer)

        elif request.POST.get('approve-as-payment'):
            response = approve_as_payment(request, customer)

        elif request.POST.get('reject_estimate'):
            response = reject_estimate(request, customer)

        elif request.POST.get('edit_job'):
            response = edit_job(request, customer)

        if request.is_ajax():
            return HttpResponse(response)
        else:
            return redirect(response)

    else: # if a GET (or any other method) we'll create a blank form
        approve_form = Approve_Job()
        approve_as_payment_form = Approve_As_Payment()
        edit_job_form = Edit_Job(user=request.user)
        reject_estimate_form = Reject_Estimate()

    return HttpResponse(template.render(context, request))
