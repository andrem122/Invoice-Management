from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from jobs.models import Job, House, Request_Payment, Current_Worker
from .forms import Change_Payment_Status
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import customer_and_staff_check
from customer_register.customer import Customer
from django.core.mail import send_mail
from payment_history.forms import Upload_Document_Form
from send_data.forms import Send_Data
import datetime

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def approved_payments(request):
    current_user = request.user
    customer = Customer(current_user)

    #get all houses with a payment history and approved payments for the current week
    houses = customer.payment_history_houses()
    payments = customer.current_payments()

    #get an empty form
    form = Change_Payment_Status()
    upload_document_form = Upload_Document_Form()

    template = loader.get_template('payment_requests/approved_payments.html')
    start_week = str(Customer.start_week.date())
    today = str(Customer.today.date())
    send_data_form = Send_Data()

    context = {
        'houses': houses,
        'payments': payments,
        'current_user': current_user,
        'form': form,
        'upload_document_form': upload_document_form,
        'start_week': start_week,
        'today': today,
        'send_data_form': send_data_form,
    }

    #form logic for unapproving payments
    if request.method == 'POST':
        form = Change_Payment_Status(request.POST)

        if form.is_valid():
            p_id = int(request.POST.get('p_id'))
            job_id = int(request.POST.get('job_id'))
            address = str(request.POST.get('job_house'))

            house = House.objects.get(address=address)
            payment = Request_Payment.objects.get(pk=p_id)
            request_amount = payment.amount

            #subtract from the total_paid column in the Job table
            job = Job.objects.get(pk=job_id)
            total_paid = job.total_paid

            #find new total paid
            new_total_paid = total_paid - request_amount

            #update approved column to False for the specific payment and job and subtract from the total_paid column
            job.total_paid = new_total_paid
            payment.approved = False
            house.pending_payments = True

            #update the balance_amount column AFTER updating the total_paid column
            job.balance_amount = job.balance

            #if job balance greater than zero, add as current worker
            if job.balance_amount > 0:
                worker, created = Current_Worker.objects.get_or_create(
                    company=job.company,
                    house=house,
                    current=True,
                )

            job.save()
            payment.save()

            """
            if no more completed jobs for the house, set completed_jobs=False
            """
            if not Job.objects.filter(house=house, approved=True, balance_amount__lte=0).exists():
                house.completed_jobs = False

            """if there are no more approved payments for a house,
            set payment_history=False for the house
            """
            if not Request_Payment.objects.filter(house=house, approved=True).exists():
                house.payment_history = False

            house.save()

            return redirect('/payment_requests/approved_payments')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Change_Payment_Status()

    return HttpResponse(template.render(context, request))

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def unapproved_payments(request):
    #get all houses that have payment requests
    current_user = request.user
    customer = Customer(current_user)

    #get all unapproved payments and houses with pending payments
    houses = customer.current_payment_requests_houses()
    payments = customer.current_payment_requests()
    start_week = str(Customer.start_week.date())
    today = str(Customer.today.date())

    #get an empty form
    form = Change_Payment_Status()
    send_data_form = Send_Data()

    template = loader.get_template('payment_requests/unapproved_payments.html')

    context = {
        'houses': houses,
        'payments': payments,
        'current_user': current_user,
        'form': form,
        'start_week': start_week,
        'today': today,
        'send_data_form': send_data_form,
    }

    #form logic
    if request.method == 'POST':
        #get populated form
        form = Change_Payment_Status(request.POST)

        if form.is_valid():
            #get job ID from POST
            p_id = int(request.POST.get('p_id'))
            job_id = int(request.POST.get('job_id'))
            address = str(request.POST.get('job_house'))

            house = House.objects.filter(address=address)

            payment = Request_Payment.objects.filter(id=p_id)
            request_amount = payment[0].amount

            #add to the total_paid column in the Job table
            job = Job.objects.filter(id=job_id)
            total_paid = job[0].total_paid

            #find new total paid
            new_total_paid = total_paid + request_amount

            """update approved column to True and set approved_date to the time the payment was
            approved and update the total_paid column for the job"""
            job.update(total_paid=new_total_paid)
            payment.update(approved=True, approved_date=datetime.datetime.now())

            #update the balance_amount column AFTER updating the total_paid column
            job.update(balance_amount=job[0].balance)

            #since a payment was approved, set payment history to true
            house.update(payment_history=True)

            #if balance is less than or equal to zero, set completed_jobs=True
            if job[0].balance <= 0:
                house.update(completed_jobs=True)


            """if there are no more unapproved payments for a house,
            set pending_payments=False for that specific house
            AND if a company has no more jobs for a house with a balance greater than zero,
            then delete them as a current_worker
            """
            flags = [
                        Request_Payment.objects.filter(house=house[0], approved=False),
                        Job.objects.filter(company=job[0].company, house=job[0].house, balance_amount__gt=0),
                    ]

            if not flags[0]:
                house.update(pending_payments=False, payment_history=True)
            if not flags[1]:
                worker = Current_Worker.objects.filter(company=job[0].company, house=job[0].house)
                worker.delete()

            #send approval email to worker
            message = """Hi {},\n\nA payment of ${} for your job at {} has been approved.\n\nThanks for your cooperation.\nNecro Software Systems
            """.format(job[0].company.get_username(), job[0].start_amount, job[0].house.address)
            try:
                send_mail(
                    'Payment Approved!',
                    message,
                    current_user.email,
                    [job[0].company.email],
                    fail_silently=False,
                )
            except:
                print('Email has failed')

            return redirect('/payment_requests/unapproved_payments')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Change_Payment_Status()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('payment_requests/thank_you.html')
    return HttpResponse(template.render(request=request))
