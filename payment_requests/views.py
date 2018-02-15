from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from jobs.models import Job, House, Request_Payment
from .forms import Approve_Payment
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def approved_payments(request):
    #get all houses that have payment requests
    current_user = request.user

    if current_user.is_active and current_user.is_staff:
        houses = House.objects.filter(payment_history=True)

        #get all approved payments
        payments = Request_Payment.objects.filter(approved=True)

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

                #update approved column to True for the specific payment and add to the total_paid column
                job.update(total_paid=new_total_paid)
                payment.update(approved=False)
                house.update(pending_payments=True)

                #update the balance_amount column AFTER updating the total_paid column
                job.update(balance_amount=job[0].balance)

                """if there are no more approved payments for a house,
                set payment_history=False for that specific house
                """
                payments = Request_Payment.objects.filter(house=house[0], approved=True)

                if not payments:
                    house.update(pending_payments=True, payment_history=False)


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
            houses = House.objects.filter(pending_payments=True)

            #get all unapproved payments
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
                    payment.update(approved=True, approved_date=datetime.now())

                    #update the balance_amount column AFTER updating the total_paid column
                    job.update(balance_amount=job[0].balance)

                    #since a payment was approved, set payment history to true
                    house.update(payment_history=True)


                    """if there are no more unapproved payments for a house,
                    set pending_payments=False for that specific house
                    """
                    payments = Request_Payment.objects.filter(house=house[0], approved=False)

                    if not payments:
                        house.update(pending_payments=False, payment_history=True)

            # if a GET (or any other method) we'll create a blank form
            else:
                form = Approve_Payment()

            return HttpResponse(template.render(context, request))

        else:
            return HttpResponseRedirect('/accounts/login')
