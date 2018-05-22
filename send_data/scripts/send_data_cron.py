from send_data.send_data_extras import send_data_email
from customer_register.customer import Customer
from django.contrib.auth.models import User
import sys

def run():
    #get data needed to send email
    path = sys.argv[3]
    host = sys.argv[4]
    user_id = int(sys.argv[5])
    form_vals = {
        'send_to': sys.argv[6],
        'subject': 'Data',
        'message': '',
    }

    #get user for customer instance
    user = User.objects.get(pk=user_id)
    customer = Customer(user)

    #send data based on path
    if path == '/jobs_admin/':
        #get data to write to csv
        jobs = customer.approved_jobs()

        #send data
        headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid', 'Contract Link']
        attributes = [['house', 'address'], 'company', 'start_amount', 'balance', 'start_date', 'total_paid', 'document_link']
        send_data_email(user_email=user.email, title='ACTIVE JOBS', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)
        print('Email Sent')

    elif path == '/jobs_admin/proposed_jobs':
        jobs = customer.proposed_jobs()
        headers = ['House', 'Company', 'Start Amount', 'Submit Date', 'Contract Link']
        attributes = [['house', 'address'], 'company', 'start_amount', 'start_date', 'document_link']
        send_data_email(user_email=user.email, title='ESTIMATES', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)
        print('Email Sent')

    elif path == '/payment_requests/unapproved_payments':
        payments = customer.current_payment_requests()
        headers = ['House', 'Company', 'Amount', 'Submit Date', 'Contract Link']
        attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', ['job', 'document_link']]
        send_data_email(user_email=user.email, title='PAYMENT REQUESTS', headers=headers, queryset=payments, attributes=attributes, form_vals=form_vals, host=host)
        print('Email Sent')

    elif path == '/payment_requests/approved_payments':
        payments = customer.current_payments()
        headers = ['House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Contract Link']
        attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', 'approved_date', ['job', 'document_link']]
        send_data_email(user_email=user.email, title='PAYMENTS FOR THIS WEEK', headers=headers, queryset=payments, attributes=attributes, form_vals=form_vals, host=host)
        print('Email Sent')

    elif path == '/jobs_complete/':
        jobs = customer.completed_jobs()
        headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid']
        attributes = ['house', 'company', 'start_amount', 'balance', 'start_date', 'total_paid']
        send_data_email(user_email=user.email, title='COMPLETED JOBS', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)
        print('Email Sent')
