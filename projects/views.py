from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from customer_register.customer import Customer
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def projects(request):
    customer = Customer(request.user)
    """
    Show all projects the customer currently has including
    completed projects and open ones
    """
    #get all properties of the customer
    houses = customer.houses

    """
    get number of active jobs, completed jobs,
    and total amount spent for each property
    """
    num_active_jobs = customer.num_active_jobs()
    num_completed_jobs = customer.num_completed_jobs()
    zipped = zip(houses, num_active_jobs, num_completed_jobs)
    totals = customer.house_totals(houses=houses, approved=True)
    template = loader.get_template('projects/projects.html')

    context = {
        'zipped': zipped,
        'totals': totals,
    }

    return HttpResponse(template.render(context, request))
