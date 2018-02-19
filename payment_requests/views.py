from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, House, Request_Payment, Current_Worker
from .forms import Approve_Payment
from django.contrib.auth.decorators import login_required
from jobs.dates_and_times import Dates_And_Times
import datetime

@login_required
def approved_payments(request):
    #get all houses that have payment requests
    current_user = request.user

    if current_user.is_active and current_user.is_staff:

        #filter data by current week
        payments_datetime = Dates_And_Times(House.objects.all(), Request_Payment.objects.filter(approved=True), Request_Payment)
        payments_datetime.current_week_results(update_field={'payment_history': [True, False]}, approved=True, approved_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

        #get all houses with a payment history and approved payments for the current week
        houses = House.objects.filter(payment_history=True)
        payments = Request_Payment.objects.filter(approved=True, approved_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

        #get an empty form
        form = Approve_Payment()

        template = loader.get_template('payment_requests/approved_payments.html')

        context = {
            'houses': houses,
            'payments': payments,
            'current_user': current_user,
            'form': form,
        }

        #form logic for unapproving payments
        if request.method == 'POST':
            #get populated form
            form = Approve_Payment(request.POST)

            if form.is_valid():
                #get payment ID and house address from POST
                p_id = int(request.POST.get('p_id'))
                job_id = int(request.POST.get('job_id'))
                address = str(request.POST.get('job_house'))

                #get the house with the pending payment
                house = House.objects.filter(address=address)

                payment = Request_Payment.objects.filter(id=p_id)
                request_amount = payment[0].amount

                #subtract from the total_paid column in the Job table
                job = Job.objects.filter(id=job_id)
                total_paid = job[0].total_paid

                #find new total paid
                new_total_paid = total_paid - request_amount

                #update approved column to False for the specific payment and subtract from the total_paid column
                job.update(total_paid=new_total_paid)
                payment.update(approved=False)
                house.update(pending_payments=True)

                #update the balance_amount column AFTER updating the total_paid column
                job.update(balance_amount=job[0].balance)

                #if job balance greater than zero, set completed_jobs=False
                if job[0].balance_amount > 0:
                    house.update(completed_jobs=False)

                """if there are no more approved payments for a house,
                set payment_history=False for that specific house
                AND if the job now has a balance greater than zero when the
                payment is unapproved, set current=True in jobs_current_worker
                """

                flags = [
                            Request_Payment.objects.filter(house=house[0], approved=True),
                            Job.objects.filter(company=job[0].company, house=job[0].house, balance_amount__gt=0),
                        ]

                if not flags[0]:
                    house.update(pending_payments=True, payment_history=False)
                if flags[1]:
                    worker = Current_Worker.objects.filter(company=job[0].company, house=job[0].house)
                    worker.update(current=True)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Approve_Payment()

        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseRedirect('/accounts/login')

@login_required
def unapproved_payments(request):
        #get all houses that have payment requests
        current_user = request.user

        if current_user.is_active and current_user.is_staff:

            #filter data by current week
            payments_datetime = Dates_And_Times(House.objects.all(), Request_Payment.objects.filter(approved=False), Request_Payment)
            payments_datetime.current_week_results(update_field={'pending_payments': [True, False]}, approved=False, submit_date__range=[Dates_And_Times.start_week, Dates_And_Times.end_week])

            #get all unapproved payments and houses with pending payments
            houses = House.objects.filter(pending_payments=True)
            payments = Request_Payment.objects.filter(approved=False)

            #get an empty form
            form = Approve_Payment()

            template = loader.get_template('payment_requests/unapproved_payments.html')

            context = {
                'houses': houses,
                'payments': payments,
                'current_user': current_user,
                'form': form,
            }

            #form logic
            if request.method == 'POST':
                #get populated form
                form = Approve_Payment(request.POST)

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
                    then set current=False for them in the table jobs_current_worker
                    """
                    flags = [
                                Request_Payment.objects.filter(house=house[0], approved=False),
                                Job.objects.filter(company=job[0].company, house=job[0].house, balance_amount__gt=0),
                            ]

                    if not flags[0]:
                        house.update(pending_payments=False, payment_history=True)
                    if not flags[1]:
                        worker = Current_Worker.objects.filter(company=job[0].company, house=job[0].house)
                        worker.update(current=False)

            # if a GET (or any other method) we'll create a blank form
            else:
                form = Approve_Payment()

            return HttpResponse(template.render(context, request))

        else:
            return HttpResponseRedirect('/accounts/login')
