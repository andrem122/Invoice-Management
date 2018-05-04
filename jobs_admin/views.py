from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from jobs.models import Job, Current_Worker, House, Request_Payment
from .forms import Change_Job_Status, Approve_As_Payment, Reject_Estimate
from payment_history.forms import Payment_History_Form
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.contrib.auth.models import User
from django.core.mail import send_mail
from send_data.forms import Send_Data
from customer_register.customer import Customer

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def index(request):
    current_user = request.user
    #get all customer houses and houses with active jobs
    customer = Customer(current_user)

    current_houses = customer.current_houses()
    approved_jobs = customer.approved_jobs()

    #get the empty forms
    payment_history_form = Payment_History_Form()
    change_job_status_form = Change_Job_Status()
    send_data_form = Send_Data()

    #load template
    template = loader.get_template('jobs_admin/index.html')

    context = {
        'current_workers': current_houses,
        'jobs': approved_jobs,
        'current_user': current_user,
        'payment_history_form': payment_history_form,
        'change_job_status_form': change_job_status_form,
        'send_data_form': send_data_form,
    }

    #get the register urls if they exist
    worker_url = request.GET.get('worker_url', None)
    staff_url = request.GET.get('staff_url', None)

    if worker_url and staff_url:
        #replace '?' with '&' in staff_url
        index = staff_url.find('staff') - 1
        staff_url = staff_url[:index]+ '&' + staff_url[index+1:]

        context['worker_url'] = worker_url
        context['staff_url'] = staff_url

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
            job.save(update_fields=['approved'])

            """update house to proposed_jobs=True if the unapproved job is
            within the last 2 weeks"""
            if Customer.start_week <= job.start_date <= Customer.today:
                house.proposed_jobs=True
                house.save(update_fields=['proposed_jobs'])

            """if no more current jobs for specific house, delete as current worker
            AND if no more pending payments from other approved jobs for the house exist,
            set pending_payments=False"""
            active_jobs_for_house = Job.objects.filter(company=job.company, approved=True, house=house, balance_amount__gt=0)
            payment_requests = Request_Payment.objects.filter(house=house, job__approved=True, approved=False)

            if not active_jobs_for_house:
                Current_Worker.objects.get(company=job.company, house=house).delete()
            if not payment_requests:
                house.pending_payments=False
                house.save(update_fields=['pending_payments'])

            #redirect because Django does not get database results after form submit
            return redirect('/jobs_admin')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = Change_Job_Status()

    return HttpResponse(template.render(context, request))

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def proposed_jobs(request):
    #get current user
    current_user = request.user
    customer = Customer(current_user)

    #get all houses with unapproved jobs for only the customers houses
    houses = customer.proposed_jobs_houses()
    jobs = customer.proposed_jobs()
    start_week = str(Customer.start_week.date())
    today = str(Customer.today.date())

    #get forms and template
    change_job_status_form = Change_Job_Status()
    approve_as_payment_form = Approve_As_Payment()
    send_data_form = Send_Data()
    reject_estimate_form = Reject_Estimate()
    template = loader.get_template('jobs_admin/estimates.html')

    context = {
        'houses': houses,
        'jobs': jobs,
        'current_user': current_user,
        'change_job_status_form': change_job_status_form,
        'send_data_form': send_data_form,
        'approve_as_payment_form': approve_as_payment_form,
        'reject_estimate_form': reject_estimate_form,
        'start_week': start_week,
        'today': today,
    }

    #form logic
    if request.method == 'POST':
        if request.POST.get('change-job-status'):
            change_job_status_form = Change_Job_Status(request.POST)
            if change_job_status_form.is_valid():
                #get POST data
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
                set proposed_jobs=False
                AND if there were any requested payments because the job was previously approved,
                set pending=payments=True for the house"""
                jobs = Job.objects.filter(house=house, approved=False, start_date__range=[Customer.start_week, Customer.today])
                requested_payments = Request_Payment.objects.filter(house=house, job=job, approved=False)

                if not jobs:
                    house.proposed_jobs=False
                    house.save(update_fields=['proposed_jobs'])
                if requested_payments:
                    house.pending_payments=True
                    house.save(update_fields=['pending_payments'])

                message = """Hi {},\n\nYour job at {} for ${} has been approved.\n\nThanks for your cooperation.\nNecro Software Systems
                """.format(job.company.get_username(), job.house.address, job.start_amount)
                try:
                    send_mail(
                        'Job Approved!',
                        message,
                        current_user.email,
                        [job.company.email],
                        fail_silently=False,
                    )
                except:
                    print('Email has failed')

                return redirect('/jobs_admin/proposed_jobs')

        elif request.POST.get('approve-as-payment'):
            approve_as_payment_form = Approve_As_Payment(request.POST)
            if approve_as_payment_form.is_valid():
                #get POST data
                job_id = int(request.POST.get('job_id'))
                address = request.POST.get('job_house')
                submit_date = request.POST.get('submit_date')
                amount = float(request.POST.get('amount'))

                #get the job and house
                job = Job.objects.get(pk=job_id)
                house = House.objects.get(address=address)

                #add payment to database
                Request_Payment.objects.create(job=job, submit_date=submit_date, house=house, amount=amount, approved=True)

                #update total paid for job
                total_paid = float(job.total_paid)
                job.total_paid = total_paid + amount
                job.balance_amount = job.balance
                job.approved = True
                job.save()

                #update house to have a payment history
                house.payment_history = True

                #update house to have completed jobs if balance is <= 0
                if job.balance <= 0:
                    house.completed_jobs = True

                house.save()

                #send approval email to worker
                message = """Hi {},\n\nA payment of ${} for your job at {} has been approved.\n\nThanks for your cooperation.\nNecro Software Systems
                """.format(job.company.get_username(), job.start_amount, job.house.address)
                try:
                    send_mail(
                        'Payment Approved!',
                        message,
                        current_user.email,
                        [job.company.email],
                        fail_silently=False,
                    )
                except:
                    print('Email has failed')

        elif request.POST.get('reject-estimate'):
            reject_estimate_form = Reject_Estimate(request.POST)
            if reject_estimate_form.is_valid():
                #get POST data
                job_id = int(request.POST.get('job_id'))

                #get the job
                job = Job.objects.get(pk=job_id)

                #set rejected equal to True for the estimate/job
                job.rejected = True
                job.save(update_fields=['rejected'])

    # if a GET (or any other method) we'll create a blank form
    else:
        change_job_status_form = Change_Job_Status()
        approve_as_payment_form = Approve_As_Payment()
    return HttpResponse(template.render(context, request))
