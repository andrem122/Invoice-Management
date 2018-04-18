from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from customer_register.customer import Customer

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
    totals = customer.house_totals(houses=houses)
    template = loader.get_template('projects/projects.html')

    context = {
        'zipped': zipped,
        'totals': totals,
    }

    return HttpResponse(template.render(context, request))
