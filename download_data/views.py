from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import Download_Data_Form
from django.contrib.auth.decorators import login_required
from customer_register.customer import Customer
import csv

@login_required
def index(request):
    #current user
    current_user = request.user
    if current_user.is_active and current_user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        customer = Customer(current_user)
        approved_jobs = customer.approved_jobs()
        proposed_jobs = customer.proposed_jobs()
        completed_jobs = customer.completed_jobs()
        all_payments = customer.all_payments()

        #form logic
        if request.method == 'POST':
            #get form with data
            download_data_form = Download_Data_Form(request.POST)

            if download_data_form.is_valid():
                #write to csv
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="all_data.csv"'
                writer = csv.writer(response)

                def write_to_csv(title, headers, queryset, attributes):
                    if queryset:
                        writer.writerow([title])
                        writer.writerow(headers)
                        atts = []
                        for q in queryset:
                            atts = []
                            for attribute in attributes:
                                if isinstance(attribute, list):
                                    a = str(getattr(getattr(q, attribute[0]), attribute[1]))
                                else:
                                    a = str(getattr(q, attribute))
                                atts.append(a)
                            writer.writerow(atts)

                #active jobs
                headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid']
                attributes = ['house', 'company', 'start_amount', 'balance', 'start_date', 'total_paid']
                write_to_csv(title='ACTIVE JOBS', headers=headers, queryset=approved_jobs, attributes=attributes)

                #proposed jobs
                write_to_csv(title='ESTIMATES', headers=headers, queryset=proposed_jobs, attributes=attributes)

                #completed jobs
                write_to_csv(title='COMPLETED JOBS', headers=headers, queryset=completed_jobs, attributes=attributes)

                #all payments
                headers = ['House', 'Company', 'Submit Date', 'Date Approved', 'Amount', 'Approved']
                attributes = ['house', ['job', 'company'], 'submit_date', 'approved_date', 'amount', 'approved']
                write_to_csv(title='ALL PAYMENTS', headers=headers, queryset=all_payments, attributes=attributes)

                return response

        # if a GET (or any other method), we'll create a blank form
        else:
            download_data_form = Download_Data_Form()
    else:
        return redirect('/accounts/login')
