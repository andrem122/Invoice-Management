from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import Download_Data_Form
from django.contrib.auth.decorators import login_required
from customer_register.customer import Customer
from send_data.send_data_extras import get_attributes_and_headers
from django.db.models.query import QuerySet
import csv

def write_to_csv(writer, title, queryset, request):
    if queryset:
        if isinstance(queryset, QuerySet) or isinstance(queryset, list):
            writer.writerow([title])
            for count, item in enumerate(queryset):
                headers, attributes = get_attributes_and_headers(object=item, request=request)

                #write headers for spreadsheet on first loop
                if count == 0:
                    writer.writerow(headers)

                writer.writerow(attributes)

        else:
            raise TypeError('Queryset argument must be of type Queryset or list')
    else:
        raise ValueError('A queryset must be inserted to generate a spreadsheet')

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
        expenses = customer.all_expenses()

        #form logic
        if request.method == 'POST':
            #get form with data
            download_data_form = Download_Data_Form(request.POST)

            if download_data_form.is_valid():
                #write to csv
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="all_data.csv"'
                writer = csv.writer(response)

                titles    = ('ACTIVE JOBS', 'ESTIMATES', 'COMPLETED JOBS', 'ALL PAYMENTS', 'EXPENSES')
                querysets = (approved_jobs, proposed_jobs, completed_jobs, all_payments, expenses)
                zipped    = zip(titles, querysets)

                try:
                    for title, queryset in zipped:
                        write_to_csv(
                            writer=writer,
                            title=title,
                            queryset=queryset,
                            request=request
                        )
                except ValueError as e:
                    print(e)

                return response

        # if a GET (or any other method), we'll create a blank form
        else:
            download_data_form = Download_Data_Form()
    else:
        return redirect('/accounts/login')
