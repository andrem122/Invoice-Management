from django.http import HttpResponse
from django.template import loader
from jobs.models import Job, Request_Payment, Current_Worker
from .forms import Change_Payment_Status
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import customer_and_staff_check
from customer_register.customer import Customer
from django.core.mail import send_mail
from payment_history.forms import Upload_Document_Form
from django.core.exceptions import ObjectDoesNotExist
from send_data.forms import Send_Data
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
import datetime

def load_ajax_results(user):
    customer = Customer(user)

    payment_history_houses = customer.current_week_payment_history_houses()
    payment_request_houses = customer.current_week_payment_requests_houses()
    rejected_payment_houses = customer.current_week_rejected_payment_houses()
    expenses_houses = customer.expenses_houses_pay()

    #get all payments and expenses for current week
    payments = customer.current_week_payments_all()
    #expenses = customer.current_week_expenses(pay_this_week=True)

    #combine querysets and keep unique items
    houses = set(chain(payment_history_houses, payment_request_houses, rejected_payment_houses))

    results_context = {
        'houses': houses,
        'payments': payments,
        'current_user': user,
    }

    return render_to_string('payment_requests/payments_results.html', results_context)
    
@csrf_exempt
@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def payments(request):
    current_user = request.user
    customer = Customer(current_user)

    """
    get all rejected houses, houses with a payment history, pending payments,
    and expenses for the current week
    """
    payment_history_houses = customer.current_week_payment_history_houses()
    payment_request_houses = customer.current_week_payment_requests_houses()
    rejected_payment_houses = customer.current_week_rejected_payment_houses()
    expenses_houses = customer.expenses_houses_pay()

    #get all payments and expenses for current week
    payments = customer.current_week_payments_all()
    expenses = customer.current_week_expenses(pay_this_week=True)

    #combine querysets and keep unique items
    houses = set(chain(payment_history_houses, payment_request_houses, rejected_payment_houses))

    #get an empty form
    change_payment_status_form = Change_Payment_Status()
    upload_document_form = Upload_Document_Form()

    template = loader.get_template('payment_requests/payments.html')
    start_week = str(Customer.start_week.strftime('%b %d'))
    today = str(Customer.today.strftime('%b %d'))
    send_data_form = Send_Data()

    context = {
        'houses': houses,
        'payments': payments,
        'expenses': expenses,
        'expenses_houses': expenses_houses,
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

                """update approved column to True and set approved_date to the time the payment was
                approved and update the total_paid column for the job"""
                job.total_paid = job.total_paid + payment.amount
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
                    try:
                        Current_Worker.objects.get(company=job.company, house=job.house)
                    except ObjectDoesNotExist as e:
                        print(e)

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

                if request.is_ajax():
                    html = load_ajax_results(current_user)
                    return HttpResponse(html)
                else:
                    return redirect('/payments/')

        elif request.POST.get('reject_payment'):
            change_payment_status_form = Change_Payment_Status(request.POST)

            if change_payment_status_form.is_valid():
                #get POST data
                p_id = int(request.POST.get('p_id'))

                #get objects
                payment = Request_Payment.objects.get(pk=p_id)
                job = payment.job
                house = job.house

                #find new total paid for job

                if job.balance_amount < job.start_amount:
                    job.total_paid = job.total_paid - payment.amount
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
                    house.rejected_payments = True

                #if job balance greater than zero after rejection, add as current worker
                if job.balance_amount > 0 and payment.requested_by_worker == True:
                    worker, created = Current_Worker.objects.get_or_create(
                        company=job.company,
                        house=house,
                        current=True,
                    )
                job.save(update_fields=['approved', 'rejected'])

                if payment.requested_by_worker == True:
                    payment.save(update_fields=['approved', 'rejected'])

                """
                if no more completed jobs for the house, set completed_jobs=False
                """
                if not Job.objects.filter(house=house, approved=True, balance_amount__lte=0).exists():
                    house.completed_jobs = False

                """if there are no more rejected or approved payments for the house,
                set payment_history/rejected_payments=False for the house
                """
                if not Request_Payment.objects.filter(house=house, approved=True).exists():
                    house.payment_history = False

                if not customer.current_week_rejected_payments(house=house).exists():
                    house.rejected_payments = False
                    house.save(update_fields=['rejected_payments'])

                house.save()

                if request.is_ajax():
                    html = load_ajax_results(current_user)
                    return HttpResponse(html)
                else:
                    return redirect('/payments/')

    # if a GET (or any other method) we'll create a blank form
    else:
        change_payment_status_form = Change_Payment_Status()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('payment_requests/thank_you.html')
    return HttpResponse(template.render(request=request))
