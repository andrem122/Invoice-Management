from django.shortcuts import render, redirect
from django.template import loader
from customer_register.customer import Customer
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from django.contrib import messages
from .send_data_extras import send_data_email, generate_csv, generate_zip
from django.core.mail import EmailMessage
from itertools import chain

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
                if path == '/jobs-admin/':
                    #get data to write to csv
                    estimates = customer.current_week_proposed_jobs()
                    approved_jobs = customer.approved_jobs()
                    completed_jobs = customer.current_week_completed_jobs()
                    rejected_jobs = customer.current_week_rejected_jobs()

                    jobs = list(chain(estimates, approved_jobs, completed_jobs, rejected_jobs))

                    #send data
                    headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid', 'Contract Link']
                    attributes = [['house', 'address'], 'company', 'start_amount', 'balance', 'start_date', 'total_paid', 'document_link']
                    send_data_email(user_email=current_user.email, title='ACTIVE JOBS', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)

                elif path == '/payments/':
                    #get querysets
                    payments = customer.current_week_approved_payments()
                    expenses = customer.current_week_expenses(pay_this_week=True)

                    #generate csvs
                    title = 'PAYMENTS FOR THE WEEK'
                    headers = ['House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Contract Link']
                    attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', 'approved_date', ['job', 'document_link']]
                    payments_result = generate_csv(title, headers, payments, attributes, host)

                    title = 'EXPENSES FOR THE WEEK'
                    headers = ['House', 'Expense Type', 'Amount',  'Date Added']
                    attributes = ['house', 'expense_type', 'amount', 'submit_date']
                    expenses_result = generate_csv(title, headers, expenses, attributes, host)

                    #generate zip
                    try:
                        zip_file = generate_zip(payments_result[0] + expenses_result[0])
                    except TypeError as e:
                        print('There are no query results for either payments or expenses')
                        try:
                            zip_file = generate_zip(payments_result[0])
                        except TypeError as e:
                            print('There are no query results for payments')
                            zip_file = generate_zip(expenses_result[0])


                    #create email
                    email = EmailMessage(form_vals['subject'], form_vals['message'], current_user.email, [form_vals['send_to']])

                    #attach files
                    try:
                        email.attach('payments.csv', payments_result[1], 'text/csv')
                    except TypeError as e:
                        print('No query results for payments, and therefore a CSV file could not be generated')

                    try:
                        email.attach('expenses.csv', expenses_result[1], 'text/csv')
                    except TypeError as e:
                        print('No query results for expenses, and therefore a CSV file could not be generated')

                    email.attach('files.zip', zip_file, 'application/x-zip-compressed')

                    #send email
                    email.send(fail_silently=False)

                elif path == '/jobs-complete/':
                    jobs = customer.completed_jobs()
                    headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid']
                    attributes = ['house', 'company', 'start_amount', 'balance', 'start_date', 'total_paid']
                    send_data_email(user_email=current_user.email, title='COMPLETED JOBS', headers=headers, queryset=jobs, attributes=attributes, form_vals=form_vals, host=host)

                elif path == '/expenses/':
                    expenses = customer.all_expenses()
                    headers = ['House', 'Expense Type', 'Amount',  'Date Added', 'Document Link']
                    attributes = ['house', 'expense_type', 'amount', 'submit_date', 'document_link']
                    send_data_email(user_email=current_user.email, title='EXPENSES', headers=headers, queryset=expenses, attributes=attributes, form_vals=form_vals, host=host)

            else:
                messages.error(request, 'Please enter an email address to send the data to.')
                return redirect(path)
        else:
            messages.error(request, 'Please check all fields, and try again.')
            return redirect(path)
    else:
        send_data_form = Send_Data()

    return redirect('/payment-history/thank-you')
