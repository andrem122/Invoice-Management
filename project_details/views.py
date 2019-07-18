from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
from jobs.models import House, Job
from expenses.models import Expenses
from expenses.forms import Edit_Expense
from jobs_admin.forms import Edit_Job
from django.core.paginator import Paginator
from itertools import chain

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def project_details(request, house_id):
    #get current user
    current_user = request.user

    #get forms and template
    send_data_form = Send_Data()
    edit_expense_form = Edit_Expense(user=current_user)
    edit_job_form = Edit_Job(user=current_user)
    template = loader.get_template('project_details/project_details.html')

    context = {
        'current_user': current_user,
        'send_data_form': send_data_form,
        'edit_job_form': edit_job_form,
        'edit_expense_form': edit_expense_form,
    }

    if house_id:
        #get house
        house = (
            House.objects
            .filter(pk=house_id)
            .add_budget_balance()
            .add_potential_profit()
        )[0]

        approved_jobs = Job.objects.filter(house=house, approved=True).add_balance().order_by('job_type')

        expenses = Expenses.objects.filter(house=house)
        expenses_and_jobs_list = list(chain(expenses, approved_jobs))
        paginator = Paginator(expenses_and_jobs_list, 25) #25 items per page

        page = request.GET.get('page')
        expenses_and_jobs = paginator.get_page(page)

        #add info to the context dictionary
        context['address'] = house.address
        context['house_id'] = house.id
        context['expenses_and_jobs'] = expenses_and_jobs
        context['budget_balance'] = house.budget_balance
        context['budget_balance_degree'] = house.budget_balance_degree
        context['total_spent'] = house.total_spent
        context['purchase_price'] = house.purchase_price
        context['after_repair_value'] = house.after_repair_value
        context['potential_profit'] = house.potential_profit
        context['post_from_url'] = request.build_absolute_uri()

    return HttpResponse(template.render(context, request))
