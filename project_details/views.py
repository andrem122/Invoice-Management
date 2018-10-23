from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from jobs.models import House
from .house import _House

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def project_details(request, house_id):
    #get current user
    current_user = request.user

    #get forms and template
    send_data_form = Send_Data()
    template = loader.get_template('project_details/project_details.html')

    context = {
        'current_user': current_user,
        'send_data_form': send_data_form,
    }

    if house_id:
        #get House ID from url
        house_id = int(house_id)

        #get house object
        house = House.objects.get(pk=house_id)
        address = house.address
        purchase_price = house.purchase_price
        after_repair_value = house.after_repair_value
        profit = house.profit

        #plug house object into our _House class
        house = _House(house)

        #expenses
        expenses = house.expenses()
        approved_jobs = house.approved_jobs()
        budget = house.budget()
        total_spent = house.total_spent()
        budget_balance = house.budget_balance()
        potential_profit = house.potential_profit()

        #add info to the context dictionary
        context['address'] = address
        context['expenses'] = expenses
        context['approved_jobs'] = approved_jobs
        context['budget'] = budget
        context['budget_balance'] = budget_balance[0]
        context['budget_balance_degree'] = budget_balance[1]
        context['total_spent'] = total_spent
        context['purchase_price'] = purchase_price
        context['after_repair_value'] = after_repair_value
        context['profit'] = profit
        context['potential_profit'] = potential_profit

    return HttpResponse(template.render(context, request))
