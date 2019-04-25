from django.shortcuts import render, redirect
from django.template import loader
from customer_register.customer import Customer
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from django.contrib import messages
from .send_data_extras import generate_csv, generate_zip
from django.core.mail import EmailMessage
from django.conf import settings
import sys
from itertools import chain

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def send_data(request):
    current_user = request.user
    customer = Customer(current_user)

    #get an empty form
    send_data_form = Send_Data()

    if request.method == 'POST':
        send_data_form = Send_Data(request.POST)
        path = str(request.POST.get('path', None))
        if send_data_form.is_valid():
            #get form data
            send_to   = str(send_data_form.cleaned_data['send_to'])
            message   = str(send_data_form.cleaned_data['message'])
            approved  = send_data_form.cleaned_data['approved']
            rejected  = send_data_form.cleaned_data['rejected']
            new       = send_data_form.cleaned_data['new']
            completed = send_data_form.cleaned_data['completed']

            statuses = {
                'approved': approved,
                'rejected': rejected,
                'new': new,
                'completed': completed,
            }

            form_vals = {
                'send_to': send_to,
                'message': message,
            }

            if send_to:
                #send data based on path
                if path == '/jobs-admin/':
                    #get data to write to csv
                    approved_jobs = customer.approved_jobs()
                    rejected_jobs = customer.current_week_rejected_jobs()
                    estimates = customer.current_week_proposed_jobs()
                    completed_jobs = customer.current_week_completed_jobs()

                    email = EmailMessage(
                        'Shared Data',
                        form_vals['message'],
                        settings.EMAIL_HOST_USER,
                        [form_vals['send_to']]
                    )

                    """
                    if all status values in 'statuses' dict are False, send all weekly jobs
                    OR
                    if all status values are in 'statuses' dict are True, send all weekly jobs
                    """
                    status_values = statuses.values()
                    if True not in status_values or all(status_value == True for status_value in status_values):
                        jobs = list(chain(estimates, approved_jobs, completed_jobs, rejected_jobs))
                        csv = generate_csv(title='ALL WEEKLY JOBS', queryset=jobs, request=request)
                        zip_file = generate_zip(queryset=jobs)
                        email.attach('data.csv', csv, 'text/csv')
                        email.attach('files.zip', zip_file, 'application/x-zip-compressed')
                    else:
                        for status_name, status_value in statuses.items():
                            if status_name == 'approved' and status_value == True and approved_jobs:
                                csv = generate_csv(title='ALL WEEKLY APPROVED JOBS', queryset=approved_jobs, request=request)
                                zip_file = generate_zip(queryset=approved_jobs)
                                email.attach('approved.csv', csv, 'text/csv')
                                email.attach('approved.zip', zip_file, 'application/x-zip-compressed')

                            elif status_name == 'rejected' and status_value == True and rejected_jobs:
                                csv = generate_csv(title='ALL WEEKLY REJECTED JOBS', queryset=rejected_jobs, request=request)
                                zip_file = generate_zip(queryset=rejected_jobs)
                                email.attach('rejected.csv', csv, 'text/csv')
                                email.attach('rejected.zip', zip_file, 'application/x-zip-compressed')

                            elif status_name == 'new' and status_value == True and estimates:
                                csv = generate_csv(title='ALL WEEKLY ESTIMATES', queryset=estimates, request=request)
                                zip_file = generate_zip(queryset=estimates)
                                email.attach('estimates.csv', csv, 'text/csv')
                                email.attach('estimates.zip', zip_file, 'application/x-zip-compressed')

                            elif status_name == 'completed' and status_value == True and completed_jobs:
                                csv = generate_csv(title='ALL WEEKLY COMPLETED JOBS', queryset=completed_jobs, request=request)
                                zip_file = generate_zip(queryset=completed_jobs)
                                email.attach('completed.csv', csv, 'text/csv')
                                email.attach('completed.zip', zip_file, 'application/x-zip-compressed')

                            else:
                                print('No specific status was selected')

                    email.send(fail_silently=False)

                elif path == '/payments/':
                    #get querysets
                    payments = customer.current_week_payments_all()
                    approved_payments = customer.current_week_approved_payments()
                    rejected_payments = customer.current_week_rejected_payments()
                    new_payments = customer.current_week_new_payment_requests()
                    expenses = customer.current_week_expenses(pay_this_week=True)

                    #create email object
                    email = EmailMessage('Shared Data', form_vals['message'], current_user.email, [form_vals['send_to']])

                    status_values = statuses.values()
                    if True not in status_values or all(status_value == True for status_value in status_values):
                        payments_and_expenses = list(chain(payments, expenses))
                        csv = generate_csv(title='ALL WEEKLY PAYMENTS AND EXPENSES', queryset=payments_and_expenses, request=request)
                        zip_file = generate_zip(queryset=payments_and_expenses)
                        email.attach('data.csv', csv, 'text/csv')
                        email.attach('files.zip', zip_file, 'application/x-zip-compressed')
                    else:
                        for status_name, status_value in statuses.items():
                            if status_name == 'approved' and status_value == True and approved_payments:
                                csv = generate_csv(title='ALL WEEKLY APPROVED PAYMENTS', queryset=approved_payments, request=request)
                                zip_file = generate_zip(queryset=approved_payments)
                                email.attach('approved.csv', csv, 'text/csv')
                                email.attach('approved.zip', zip_file, 'application/x-zip-compressed')

                            elif status_name == 'rejected' and status_value == True and rejected_payments:
                                csv = generate_csv(title='ALL WEEKLY REJECTED PAYMENTS', queryset=rejected_payments, request=request)
                                zip_file = generate_zip(queryset=rejected_payments)
                                email.attach('rejected.csv', csv, 'text/csv')
                                email.attach('rejected.zip', zip_file, 'application/x-zip-compressed')

                            elif status_name == 'new' and status_value == True and new_payments:
                                csv = generate_csv(title='ALL WEEKLY NEW PAYMENT REQUESTS', queryset=new_payments, request=request)
                                zip_file = generate_zip(queryset=new_payments)
                                email.attach('new.csv', csv, 'text/csv')
                                email.attach('new.zip', zip_file, 'application/x-zip-compressed')

                            else:
                                print('No specific status was selected')


                    email.send(fail_silently=False)

            else:
                messages.error(request, 'Please enter an email address to send the data to.')
                return redirect(path)
        else:
            messages.error(request, 'Please check all fields, and try again.')
            return redirect(path)
    else:
        send_data_form = Send_Data()

    return redirect('/payment-history/thank-you')
