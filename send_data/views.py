from django.shortcuts import render, redirect
from django.template import loader
from customer_register.customer import Customer
from jobs.models import Job
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from django.contrib import messages
from .send_data_extras import send_data_email, setup_cron_job


@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def send_data(request):
    current_user = request.user
    customer = Customer(current_user)

    #get an empty form
    send_data_form = Send_Data()

    if request.method == 'POST':
        send_data_form = Send_Data(request.POST)
        path = str(request.POST.get('path', ''))
        if send_data_form.is_valid():
            #get form data
            send_to = str(send_data_form.cleaned_data['send_to'])
            subject = str(send_data_form.cleaned_data['subject'])
            message = str(send_data_form.cleaned_data['message'])
            #frequency = int(send_data_form.cleaned_data['frequency'])

            form_vals = {
                'send_to': send_to,
                'subject': subject,
                'message': message,
            }

            if send_to:
                host = request.get_host()
                #send data based on path
                if path == '/jobs_admin/':
                    #get data to write to csv
                    jobs = customer.approved_jobs()

                    #send data
                    headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid', 'Contract Link']
                    attributes = [['house', 'address'], 'company', 'start_amount', 'balance', 'start_date', 'total_paid', 'document_link']
                    send_data_email(user_email=current_user.email, title='ACTIVE JOBS', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)

                elif path == '/jobs_admin/proposed_jobs':
                    jobs = customer.proposed_jobs()
                    headers = ['House', 'Company', 'Start Amount', 'Submit Date', 'Contract Link']
                    attributes = [['house', 'address'], 'company', 'start_amount', 'start_date', 'document_link']
                    send_data_email(user_email=current_user.email, title='ESTIMATES', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)

                elif path == '/payment_requests/unapproved_payments':
                    payments = customer.current_payment_requests()
                    headers = ['House', 'Company', 'Amount', 'Submit Date', 'Contract Link']
                    attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', ['job', 'document_link']]
                    send_data_email(user_email=current_user.email, title='PAYMENT REQUESTS', headers=headers, queryset=payments, attributes=attributes, form_vals=form_vals, host=host)

                elif path == '/payment_requests/approved_payments':
                    payments = customer.current_payments()
                    headers = ['House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Contract Link']
                    attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', 'approved_date', ['job', 'document_link']]
                    send_data_email(user_email=current_user.email, title='PAYMENTS FOR THIS WEEK', headers=headers, queryset=payments, attributes=attributes, form_vals=form_vals, host=host)

                elif path == '/jobs_complete/':
                    jobs = customer.completed_jobs()
                    headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid']
                    attributes = ['house', 'company', 'start_amount', 'balance', 'start_date', 'total_paid']
                    send_data_email(user_email=current_user.email, title='COMPLETED JOBS', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)

            else:
                messages.error(request, 'Please enter an email address to send the data to.')
                return redirect(path)
        else:
            messages.error(request, 'Please check all fields, and try again.')
            return redirect(path)
    else:
        send_data_form = Send_Data()

    return redirect('/payment_history/thank_you')
