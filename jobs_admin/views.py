from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from jobs.models import Job, Current_Worker, House, Request_Payment
from project_details.house import _House
from .forms import Approve_Job, Approve_As_Payment, Reject_Estimate, Edit_Job
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.core.mail import send_mail
from send_data.forms import Send_Data
from django.core.exceptions import ObjectDoesNotExist
from customer_register.customer import Customer
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from itertools import chain

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
    plain_message = """Hi {},\n\nYour job at {} for ${} has been approved!\n\nThanks for your cooperation.\nNecro Software Systems\n\n**This is an automated message. Please do not reply**
    """.format(username, job_object.house.address, job_object.start_amount)
    try:
        send_mail(
            subject,
            plain_message,
            request.user.email,
            [job_object.company.email],
            fail_silently=False,
            html_message=html_message,
        )
    except:
        print('Email has failed')

def load_ajax_results(user):
    customer = Customer(user)

    #get active houses and houses with estimates
    active_houses = customer.active_houses()
    estimate_houses = customer.proposed_jobs_houses()
    completed_houses = customer.current_week_completed_houses()
    rejected_houses = customer.current_week_rejected_job_houses()

    #get estimates, approved, completed, and rejected jobs
    estimates = customer.current_week_proposed_jobs()
    approved_jobs = customer.approved_jobs()
    completed_jobs = customer.current_week_completed_jobs()
    rejected_jobs = customer.current_week_rejected_jobs()

    #get forms
    edit_job_form = Edit_Job(user=user)


    #combine querysets and keep unique values for houses
    houses = set(chain(active_houses, estimate_houses, completed_houses, rejected_houses))
    jobs = list(chain(estimates, approved_jobs, completed_jobs, rejected_jobs))

    job_results_context = {
        'houses': houses,
        'items': jobs,
        'current_user': user,
        'edit_job_form': edit_job_form,
    }

    return render_to_string('jobs_admin/jobs_admin_results.html', job_results_context)

@csrf_exempt
@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def index(request):
    #get current user
    current_user = request.user
    customer = Customer(current_user)

    #get active houses and houses with estimates
    active_houses = customer.active_houses()
    estimate_houses = customer.proposed_jobs_houses()
    completed_houses = customer.current_week_completed_houses()
    rejected_houses = customer.current_week_rejected_job_houses()

    #get estimates, approved, completed, and rejected jobs
    estimates = customer.current_week_proposed_jobs()
    approved_jobs = customer.approved_jobs()
    completed_jobs = customer.current_week_completed_jobs()
    rejected_jobs = customer.current_week_rejected_jobs()


    #combine querysets and keep unique values for houses
    houses = set(chain(active_houses, estimate_houses, completed_houses, rejected_houses))
    jobs = list(chain(estimates, approved_jobs, completed_jobs, rejected_jobs))

    start_week = str(Customer.start_week.date())
    today = str(Customer.today.date())

    #get forms and template
    approve_form = Approve_Job()
    approve_as_payment_form = Approve_As_Payment()
    reject_estimate_form = Reject_Estimate()
    edit_job_form = Edit_Job(user=current_user)
    send_data_form = Send_Data()
    template = loader.get_template('jobs_admin/jobs_admin.html')
    job_results = loader.get_template('jobs_admin/jobs_admin_results.html')

    context = {
        'houses': houses,
        'items': jobs,
        'current_user': current_user,
        'approve_form': approve_form,
        'approve_as_payment_form': approve_as_payment_form,
        'reject_estimate_form': reject_estimate_form,
        'edit_job_form': edit_job_form,
        'send_data_form': send_data_form,
        'start_week': start_week,
        'today': today,
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

    #form logic
    if request.method == 'POST':
        if request.POST.get('approve_job'):
            approve_form = Approve_Job(request.POST)
            if approve_form.is_valid():
                #get POST data
                job_id = int(request.POST.get('job_id'))

                job = Job.objects.get(pk=job_id)
                house = job.house

                #update approved column to True for the specific job
                job.approved = True
                job.rejected = False
                job.save(update_fields=['approved', 'rejected'])

                #add the user as a current worker on the house OR do nothing if they are already active
                if job.balance_amount > 0 and job.approved == True:
                    current_worker, created = Current_Worker.objects.get_or_create(house=house, job=job, company=job.company, customer=current_user, current=False)
                    current_worker.current = True
                    current_worker.save(update_fields=['current'])

                else: #this job may be complete because payments may have been made previously, so set house.completed_jobs=True
                    house.completed_jobs = True
                    house.save(update_fields=['completed_jobs'])

                if customer.current_week_payment_requests().exists(): #check if house has payment requests for current week
                    house.pending_payments = True
                    house.save(update_fields=['pending_payments'])

                if customer.current_week_approved_payments().exists(): #check if house has approved payments for current week
                    house.payment_history = True
                    house.save(update_fields=['payment_history'])

                if not customer.current_week_proposed_jobs(house=house).exists(): #check if house has estimates for current week
                    house.proposed_jobs = False
                    house.save(update_fields=['proposed_jobs'])

                #send approval email
                send_approval_mail(request, job, 'Job Approved!', 'Job Approved!')

                if request.is_ajax():
                    html = load_ajax_results(current_user)
                    return HttpResponse(html)
                else:
                    return redirect('/jobs-admin/')

        elif request.POST.get('approve-as-payment'):
            approve_as_payment_form = Approve_As_Payment(request.POST)
            if approve_as_payment_form.is_valid():
                #get POST data
                job_id = int(request.POST.get('job_id'))

                #get the job and house
                job = Job.objects.get(pk=job_id)
                house = job.house

                #amount requested for payment of job
                amount = float(job.start_amount)

                #add payment object to database
                Request_Payment.objects.create(job=job, house=house, amount=amount, approved=True)

                #update total paid for job
                total_paid = float(job.total_paid)
                job.total_paid = total_paid + amount
                job.balance_amount = job.balance
                job.approved = True
                job.save(update_fields=['total_paid', 'balance_amount', 'approved'])

                #update house to have a payment history
                house.payment_history = True
                house.save(update_fields=['payment_history'])

                #update house to have completed jobs if balance is <= 0
                if job.balance <= 0:
                    house.completed_jobs = True
                    house.save(update_fields=['completed_jobs'])
                if not customer.current_week_proposed_jobs(house=house).exists():
                    house.proposed_jobs = False
                    house.save(update_fields=['proposed_jobs'])

                #send approval email to worker
                send_approval_mail(request, job, 'Payment Approved!', 'Payment Approved!')

                if request.is_ajax():
                    html = load_ajax_results(current_user)
                    return HttpResponse(html)
                else:
                    return redirect('/jobs-admin/')

        elif request.POST.get('reject_estimate'):
            reject_estimate_form = Reject_Estimate(request.POST)
            if reject_estimate_form.is_valid():
                #get POST data
                job_id = int(request.POST.get('job_id'))

                #get the job and house
                job = Job.objects.get(pk=job_id)
                house = job.house

                #set rejected equal to True for the estimate/job
                job.approved = False
                job.rejected = True
                house.rejected_jobs = True

                #update job total paid if needed
                try:
                    payment = Request_Payment.objects.filter(job=job, requested_by_worker=False)
                    total_paid = float(job.total_paid)
                    job.total_paid = total_paid - float(payment[0].amount)
                    job.balance_amount = job.balance
                    payment.delete() #delete payments generated by system
                except IndexError as e:
                    print('No elements in the QuerySet, so an IndexError will occur')

                job.save()
                house.save(update_fields=['rejected_jobs'])

                #update current worker object current attribute to false if no active jobs exist for the house
                if not Job.objects.filter(house=job.house, house__customer=customer.customer, approved=True, balance_amount__gt=0).exists():
                    try:
                        current_worker = Current_Worker.objects.get(house=job.house, job=job, company=job.company, customer=current_user, current=True)
                        current_worker.current = False
                        current_worker.save()

                    except ObjectDoesNotExist as e:
                        print(e)

                if not customer.current_week_proposed_jobs(house=house).exists():
                    house.proposed_jobs = False
                    house.save(update_fields=['proposed_jobs'])
                if not customer.completed_jobs(house=house).exists():
                    house.completed_jobs = False
                    house.save(update_fields=['completed_jobs'])

                if request.is_ajax():
                    html = load_ajax_results(current_user)
                    return HttpResponse(html)
                else:
                    return redirect('/jobs-admin/')

        elif request.POST.get('edit_job'):
            job_id = int(request.POST.get('job_id')) #get job id from POST request
            job = get_object_or_404(Job, id=job_id) #get job instance

            edit_job_form = Edit_Job(data=request.POST, files=request.FILES, user=current_user)

            if edit_job_form.is_valid():

                previous_house = job.house #the house the job object belonged to before it is changed
                previous_company = job.company
                new_house = edit_job_form.cleaned_data.get('house', None)
                new_company = edit_job_form.cleaned_data.get('company', None)
                document_link = edit_job_form.cleaned_data.get('document_link', None)
                notes = edit_job_form.cleaned_data.get('notes', None)
                start_amount = edit_job_form.cleaned_data.get('start_amount', None)

                #update the job instance based on which fields were submitted in the form
                if new_house != None:
                    job.house = new_house

                    #update objects
                    Request_Payment.objects.filter(job__pk=job_id).update(house=new_house) #get payments associated with job instance
                    job.save(update_fields=['house'])

                    #if the company working on the previous house has no more active jobs with that house, set current to false on the current_worker object
                    if not _House(previous_house).has_active_jobs(company=job.company):
                        try:
                            current_worker = Current_Worker.objects.get(house=previous_house, job=job, company=previous_company, customer=current_user, current=True)
                            current_worker.current = False
                            current_worker.save(update_fields=['current'])

                        except ObjectDoesNotExist as e:
                            print(e)

                    #if the new house now has an active job, create a current worker object
                    if _House(new_house).has_active_jobs():

                        #if both the house and company are being changed, get the new company and use it to get or create a current_worker object
                        company = job.company
                        if new_company != None:
                            company = new_company

                        current_worker, created = Current_Worker.objects.get_or_create(house=job.house, job=job, company=company, customer=current_user, current=False)
                        #if there was a current_worker object already, get it and set current equal to True
                        current_worker.current = True
                        current_worker.save(update_fields=['current'])

                if new_company != None:

                    job.company = new_company
                    job.save(update_fields=['company'])

                    #when changing the company, set current to false for the previous current worker object and create a new worker object
                    try:
                        #get previous current_worker object
                        current_worker = Current_Worker.objects.get(house=previous_house, job=job, company=previous_company, customer=current_user, current=True)
                        current_worker.current = False
                        current_worker.save()

                        new_current_worker, created = Current_Worker.objects.get_or_create(house=job.house, job=job, company=new_company, customer=current_user, current=False)
                        #if there was a current_worker object already (current was set to False), get it and set current equal to True
                        new_current_worker.current = True
                        new_current_worker.save(update_fields=['current'])

                    except ObjectDoesNotExist as e:
                        print(e)

                if document_link != None:
                    job.document_link = document_link
                    job.save(update_fields=['document_link'])

                if notes != None:
                    job.notes = notes
                    job.save(update_fields=['notes'])

                if start_amount != None and 1 + float(start_amount) != 1.0: #update balance_amount if start_amount is in the POST data
                    job.start_amount = start_amount
                    job.balance_amount = job.balance
                    print(job.balance_amount)
                    job.save(update_fields=['start_amount', 'balance_amount'])

            else:
                print(edit_job_form.errors)


            if request.is_ajax():
                html = load_ajax_results(current_user)
                return HttpResponse(html)
            else:
                return redirect('/jobs-admin/')
    # if a GET (or any other method) we'll create a blank form
    else:
        approve_form = Approve_Job()
        approve_as_payment_form = Approve_As_Payment()
        edit_job_form = Edit_Job(user=current_user)
    return HttpResponse(template.render(context, request))
