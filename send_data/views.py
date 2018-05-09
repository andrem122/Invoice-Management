from django.shortcuts import render, redirect
from django.template import loader
from customer_register.customer import Customer
from jobs.models import Job
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from django.contrib import messages
import csv
import io
import os
import zipfile

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def send_data(request):
    current_user = request.user
    customer = Customer(current_user)

    #get an empty form
    send_data_form = Send_Data()

    def send_data(title, headers, queryset, attributes):
        if queryset:
            csv_file = io.StringIO()
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([title])
            writer.writerow(headers)
            document_links = []
            for q in queryset.iterator():
                if hasattr(q, 'document_link') and isinstance(q, Job):
                    document_links.append(str(q.document_link))
                else:
                    document_links.append(str(q.job.document_link))
                atts = []
                for attribute in attributes:
                    if isinstance(attribute, list):
                        if attribute[1] == 'document_link':
                            a = 'http://' + str(request.get_host()) + '/media/' + str(getattr(getattr(q, attribute[0]), attribute[1]))
                        else:
                            a = str(getattr(getattr(q, attribute[0]), attribute[1]))
                    else:
                        #prepend a string to the document link string
                        if attribute == 'document_link':
                            a = 'http://' + str(request.get_host()) + '/media/' + str(getattr(q, attribute))
                        else:
                            a = str(getattr(q, attribute))
                    atts.append(a)
                writer.writerow(atts)

            #create email
            email = EmailMessage(subject, message, current_user.email, [send_to])
            email.attach('data.csv', csv_file.getvalue(), 'text/csv')

            #generate zip file
            if len(document_links) != 0:
                zip_file = io.BytesIO()
                zf = zipfile.ZipFile(zip_file, "w")
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                prev_arcnames = []
                for counter, fpath in enumerate(document_links):
                    absname = os.path.abspath(os.path.join(base_dir, 'media', *fpath.split('/')))
                    arcname = os.path.split(absname)[1]

                    #do not overwrite files with the same name
                    if arcname in prev_arcnames:
                        fname, ext = os.path.splitext(arcname)
                        arcname = '{fname}-{counter}{ext}'.format(fname=fname, counter=counter, ext=ext)
                        
                    prev_arcnames.append(arcname)

                    zf.write(absname, arcname)

                zf.close()
                email.attach('files.zip', zip_file.getvalue(), 'application/x-zip-compressed')

            #send email
            email.send(fail_silently=False)

    if request.method == 'POST':
        send_data_form = Send_Data(request.POST)
        path = str(request.POST.get('path', ''))
        if send_data_form.is_valid():
            #get form data
            send_to = str(send_data_form.cleaned_data['send_to'])
            subject = str(send_data_form.cleaned_data['subject'])
            message = str(send_data_form.cleaned_data['message'])

            if send_to:
                #send data based on path
                if path == '/jobs_admin/':
                    #get data to write to csv
                    jobs = customer.approved_jobs()

                    #send data
                    headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid', 'Contract Link']
                    attributes = [['house', 'address'], 'company', 'start_amount', 'balance', 'start_date', 'total_paid', 'document_link']
                    send_data(title='ACTIVE JOBS', headers=headers, queryset=jobs, attributes=attributes)

                elif path == '/jobs_admin/proposed_jobs':
                    jobs = customer.proposed_jobs()
                    headers = ['House', 'Company', 'Start Amount', 'Submit Date', 'Contract Link']
                    attributes = [['house', 'address'], 'company', 'start_amount', 'start_date', 'document_link']
                    send_data(title='ESTIMATES', headers=headers, queryset=jobs, attributes=attributes)

                elif path == '/payment_requests/unapproved_payments':
                    payments = customer.current_payment_requests()
                    headers = ['House', 'Company', 'Amount', 'Submit Date', 'Contract Link']
                    attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', ['job', 'document_link']]
                    send_data(title='PAYMENT REQUESTS', headers=headers, queryset=payments, attributes=attributes)

                elif path == '/payment_requests/approved_payments':
                    payments = customer.current_payments()
                    headers = ['House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Contract Link']
                    attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', 'approved_date', ['job', 'document_link']]
                    send_data(title='PAYMENTS FOR THIS WEEK', headers=headers, queryset=payments, attributes=attributes)

                elif path == '/jobs_complete/':
                    jobs = customer.completed_jobs()
                    headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid']
                    attributes = ['house', 'company', 'start_amount', 'balance', 'start_date', 'total_paid']
                    send_data(title='COMPLETED JOBS', headers=headers, queryset=jobs, attributes=attributes)
                else:
                    messages.error(request, 'Something went wrong. Please try again.')
                    return redirect(path)
            else:
                messages.error(request, 'Please enter an email address to send the data to.')
                return redirect(path)
        else:
            messages.error(request, 'Please check all fields, and try again.')
            return redirect(path)
    else:
        send_data_form = Send_Data()

    return redirect('/payment_history/thank_you')
