from django.http import HttpResponse
from django.template import loader
from jobs.models import Job, Request_Payment
from search_submit.views import Search_Submit_View
from .forms import Change_Payment_Status
from expenses.forms import Delete_Expense
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import customer_and_staff_check
from customer_register.customer import Customer
from django.core.mail import send_mail
from payment_history.forms import Upload_Document_Form
from jobs_admin.forms import Approve_Job, Approve_As_Payment, Reject_Estimate, Edit_Job
from django.core.exceptions import ObjectDoesNotExist
from send_data.forms import Send_Data
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.conf import settings
from itertools import chain
from ajax.ajax import Ajax
import datetime

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

def send_approval_mail(request, payment_object, subject, html_title):
    template_message = 'Your payment request for ${} at {} has been approved!'.format(payment_object.amount, payment_object.job.house.address)
    username = payment_object.job.company.get_username()
    context = {
        'username': username,
        'template_message': template_message,
        'title': html_title,
        'host_url': request.build_absolute_uri('/'),
    }
    html_message = render_to_string('email/approved.html', context)
    plain_message = """Hi {},\n\nYour payment request for ${} at {} has been approved!\n\nThanks for your cooperation.\nNova One Software Systems\n\n**This is an automated message. Please do not reply**
    """.format(username, payment_object.amount, payment_object.job.house.address)
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [payment_object.job.company.email],
            fail_silently=False,
            html_message=html_message,
        )
    except:
        print('Email has failed')

def approve_payment(request, customer):
    change_payment_status_form = Change_Payment_Status(request.POST)

    if change_payment_status_form.is_valid():
        #get payment id from POST
        p_id = int(request.POST.get('p_id'))
        post_from_url = request.POST.get('post_from_url', None)

        payment = Request_Payment.objects.get(pk=p_id)
        job = payment.job
        house = job.house

        """update approved column to True and set approved_date to the time the payment was
        approved"""

        payment.approved_date = datetime.datetime.now()
        payment.approved = True
        payment.rejected = False
        payment.save(update_fields=['approved', 'approved_date', 'rejected'])

        #send approval email to worker
        send_approval_mail(request, payment, 'Payment Approved!', 'Payment Approved!')

        if request.is_ajax():
            if 'search' in post_from_url:
                return load_ajax_search_results(request=request)
            else:
                ajax = Ajax(customer)
                html = ajax.load_ajax_results('payments')
                return html
        else:
            return request.POST.get('post_from_url', None)


def reject_payment(request, customer):
    change_payment_status_form = Change_Payment_Status(request.POST)

    if change_payment_status_form.is_valid():
        #get POST data
        p_id = int(request.POST.get('p_id'))
        post_from_url = request.POST.get('post_from_url', None)

        #get objects
        payment = Request_Payment.objects.get(pk=p_id)
        job = payment.job
        house = job.house

        # Edit or delete objects
        if payment.created_by_system == True: #if the payment is created by the system
            payment.delete()

            if customer.current_week_approved_payments(job=job): #if there are approved or rejected payments for the job, set job.approved = True
                job.approved = True
            else:
                job.approved = False

            job.rejected = False
        else:
            payment.approved = False
            payment.rejected = True

        # Update objects if edited
        job.save(update_fields=['approved', 'rejected'])
        if payment.created_by_system == False:
            payment.save(update_fields=['approved', 'rejected'])

        # Return html if the request is AJAX else return a url if not AJAX
        if request.is_ajax():
            if 'search' in post_from_url:
                return load_ajax_search_results(request=request)
            else:
                ajax = Ajax(customer)
                html = ajax.load_ajax_results('payments')
                return html
        else:
            return request.POST.get('post_from_url', None)

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
    post_from_url = request.build_absolute_uri()
    today = str(Customer.today.strftime('%b %d'))
    send_data_form = Send_Data()

    context = {
        'houses': houses,
        'items': payments,
        'expenses': expenses,
        'expenses_houses': expenses_houses,
        'current_user': current_user,
        'change_payment_status_form': change_payment_status_form,
        'upload_document_form': upload_document_form,
        'start_week': start_week,
        'today': today,
        'post_from_url': post_from_url,
        'send_data_form': send_data_form,
    }

    #form logic for rejecting payments
    if request.method == 'POST':
        post_from_url = request.POST.get('post_from_url', None)
        response = '<h2>Error</h2>'

        if request.POST.get('approve_payment'):
            response = approve_payment(request=request, customer=customer)

        elif request.POST.get('reject_payment'):
            response = reject_payment(request=request, customer=customer)

        if request.is_ajax():
            return HttpResponse(response)
        else:
            return redirect(response)


    # if a GET (or any other method) we'll create a blank form
    else:
        change_payment_status_form = Change_Payment_Status()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('payment_requests/thank_you.html')
    return HttpResponse(template.render(request=request))
