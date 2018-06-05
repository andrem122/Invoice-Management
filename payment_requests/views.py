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
from itertools import chain
import datetime

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def approved_payments(request):
    current_user = request.user
    customer = Customer(current_user)

    #get all rejected houses, houses with a payment history, and pending payments for the current week
    payment_history_houses = customer.payment_history_houses()
    payment_request_houses = customer.current_payment_requests_houses()
    rejected_payment_houses = customer.current_week_rejected_payments_houses()

    #get all payments for current week
    payments = customer.current_week_payments_all()

    #combine querysets and keep unique houses
    houses = set(chain(payment_history_houses, payment_request_houses, rejected_payment_houses))

    #get an empty form
    change_payment_status_form = Change_Payment_Status()
    upload_document_form = Upload_Document_Form()

    template = loader.get_template('payment_requests/approved_payments.html')
    start_week = str(Customer.start_week.date())
    today = str(Customer.today.date())
    send_data_form = Send_Data()

    context = {
        'houses': houses,
        'payments': payments,
        'current_user': current_user,
        'change_payment_status_form': change_payment_status_form,
        'upload_document_form': upload_document_form,
        'start_week': start_week,
        'today': today,
        'send_data_form': send_data_form,
    }

    #form logic for rejecting payments
    if request.method == 'POST':
        if request.POST.get('approve_payment'):
            #get populated form
            change_payment_status_form = Change_Payment_Status(request.POST)

            if change_payment_status_form.is_valid():
                #get payment id from POST
                p_id = int(request.POST.get('p_id'))

                payment = Request_Payment.objects.get(pk=p_id)
                job = payment.job
                house = job.house
                request_amount = payment.amount

                #add to the total_paid column for the job
                new_total_paid = job.total_paid + request_amount

                """update approved column to True and set approved_date to the time the payment was
                approved and update the total_paid column for the job"""
                job.total_paid = new_total_paid
                job.save(update_fields=['total_paid'])
                job.balance_amount = job.balance #update the balance
                job.save(update_fields=['balance_amount'])

                payment.approved_date = datetime.datetime.now()
                payment.approved = True
                payment.rejected = False
                payment.save(update_fields=['approved', 'approved_date', 'rejected'])

                #since a payment was approved, set payment history to true
                house.payment_history = True

                #if balance is less than or equal to zero, set completed_jobs=True
                if job.balance_amount <= 0:
                    house.completed_jobs = True


                """if there are no more unapproved payments for a house,
                set pending_payments=False for that specific house
                AND if a company has no more jobs for a house with a balance greater than zero,
                then delete them as a current_worker
                """

                if not Request_Payment.objects.filter(house=house, approved=False).exists():
                    house.pending_payments = False
                if not Job.objects.filter(company=job.company, house=job.house, balance_amount__gt=0).exists():
                    worker = Current_Worker.objects.get(company=job.company, house=job.house)
                    worker.delete()

                house.save(update_fields=['pending_payments', 'payment_history', 'completed_jobs'])

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

                return redirect('/payment_requests/approved_payments')

        elif request.POST.get('reject_payment'):
            change_payment_status_form = Change_Payment_Status(request.POST)

            if change_payment_status_form.is_valid():
                #get POST data
                p_id = int(request.POST.get('p_id'))

                #get objects
                payment = Request_Payment.objects.get(pk=p_id)
                job = payment.job
                house = House.objects.get(pk=int(job.house.id))
                request_amount = payment.amount

                #find new total paid for job
                total_paid = job.total_paid
                new_total_paid = float(total_paid) - float(request_amount)
                job.total_paid = new_total_paid
                job.save(update_fields=['total_paid']) #update database value so the balance can be calculated
                job.balance_amount = job.balance #update the balance
                job.save(update_fields=['balance_amount'])

                if payment.requested_by_worker == False:
                    payment.delete()
                    job.approved = False
                    job.rejected = False
                    house.proposed_jobs = True
                else:
                    payment.approved = False
                    payment.rejected = True
                    house.pending_payments = True

                #if job balance greater than zero after rejection, add as current worker
                if job.balance_amount > 0 and payment.requested_by_worker == True:
                    worker, created = Current_Worker.objects.get_or_create(
                        company=job.company,
                        house=house,
                        current=True,
                    )
                job.save(update_fields=['approved', 'rejected'])

                if payment.requested_by_worker == True:
                    payment.save(update_fields=['approved'])

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

                house.save(update_fields=['pending_payments', 'payment_history', 'completed_jobs', 'proposed_jobs'])

                return redirect('/payment_requests/approved_payments')

    # if a GET (or any other method) we'll create a blank form
    else:
        change_payment_status_form = Change_Payment_Status()

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

            payment = Request_Payment.objects.get(pk=p_id)
            job = payment.job
            house = job.house
            request_amount = payment.amount

            #add to the total_paid column for the job
            new_total_paid = job.total_paid + request_amount

            """update approved column to True and set approved_date to the time the payment was
            approved and update the total_paid column for the job"""
            job.total_paid = new_total_paid
            job.save(update_fields=['total_paid'])
            job.balance_amount = job.balance #update the balance
            job.save(update_fields=['balance_amount'])

            payment.approved_date = datetime.datetime.now()
            payment.approved = True
            payment.rejected = False
            payment.save(update_fields=['approved', 'approved_date', 'rejected'])

            #since a payment was approved, set payment history to true
            house.payment_history = True

            #if balance is less than or equal to zero, set completed_jobs=True
            if job.balance_amount <= 0:
                house.completed_jobs = True


            """if there are no more unapproved payments for a house,
            set pending_payments=False for that specific house
            AND if a company has no more jobs for a house with a balance greater than zero,
            then delete them as a current_worker
            """

            if not Request_Payment.objects.filter(house=house, approved=False).exists():
                house.pending_payments = False
            if not Job.objects.filter(company=job.company, house=job.house, balance_amount__gt=0).exists():
                worker = Current_Worker.objects.get(company=job.company, house=job.house)
                worker.delete()

            house.save(update_fields=['pending_payments', 'payment_history', 'completed_jobs'])

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

            return redirect('/payment_requests/approved_payments')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Change_Payment_Status()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('payment_requests/thank_you.html')
    return HttpResponse(template.render(request=request))
