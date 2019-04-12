from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
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

    """
    get number of active jobs, completed jobs,
    and total amount spent for each property
    """
    archived_houses = customer.projects(archived=1)
    narchived_houses = customer.projects(archived=0)
    template = loader.get_template('projects/projects.html')
    send_data_form = Send_Data()
    archive_house_form = Archive_House()

    context = {
        'archived_houses': archived_houses,
        'narchived_houses': narchived_houses,
        'current_user': current_user,
        'archive_house_form': archive_house_form,
        'send_data_form': send_data_form,
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
        else:
            print(archive_house_form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        archive_house_form = Archive_House()

    return HttpResponse(template.render(context, request))
