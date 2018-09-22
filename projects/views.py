from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from send_data.forms import Send_Data
from .forms import Archive_House
from jobs.models import House
from customer_register.customer import Customer
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def projects(request):
    current_user = request.user
    customer = Customer(current_user)
    """
    Show all projects the customer currently has including
    completed projects and open ones
    """
    #get all houses/projects of the customer
    narchived_houses = customer._houses(archived=False)
    archived_houses = customer._houses(archived=True)

    """
    get number of active jobs, completed jobs,
    and total amount spent for each property
    """
    num_expenses = customer.num_expenses(archived=False)
    num_active_jobs = customer.num_active_jobs(archived=False)
    num_completed_jobs = customer.num_completed_jobs(archived=False)
    narchived_totals = customer.house_totals(houses=narchived_houses, approved=True)
    zipped_narchived = zip(narchived_houses, num_expenses, num_active_jobs, num_completed_jobs, narchived_totals)

    num_expenses = customer.num_expenses(archived=True)
    num_active_jobs = customer.num_active_jobs(archived=True)
    num_completed_jobs = customer.num_completed_jobs(archived=True)
    archived_totals = customer.house_totals(houses=archived_houses, approved=True)
    zipped_archived = zip(archived_houses, num_expenses, num_active_jobs, num_completed_jobs, archived_totals)


    template = loader.get_template('projects/projects.html')
    send_data_form = Send_Data()
    archive_house_form = Archive_House()

    context = {
        'zipped_narchived': zipped_narchived,
        'zipped_archived': zipped_archived,
        'archived_houses': archived_houses,
        'current_user': current_user,
        'send_data_form': send_data_form,
        'archive_house_form': archive_house_form,
    }

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        archive_house_form = Archive_House(request.POST)

        if archive_house_form.is_valid():
            #get house ID from POST request
            house_id = int(request.POST.get('house_id'))

            #store form data into variables
            house = House.objects.get(pk=house_id)

            if house.archived == False: #if house.archived is False
                house.archived = True
                house.save(update_fields=['archived'])
            else: #if house.archived is True already
                house.archived = False
                house.save(update_fields=['archived'])


            return redirect('/projects')

    # if a GET (or any other method) we'll create a blank form
    else:
        archive_house_form = Archive_House()

    return HttpResponse(template.render(context, request))
