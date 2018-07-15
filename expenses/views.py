from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from jobs.models import House
from .models import Expenses
from .forms import Delete_Expense
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from customer_register.customer import Customer
from send_data.forms import Send_Data

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def expenses(request):
    #get current user
    current_user = request.user
    customer = Customer(current_user)

    #get houses with expenses
    houses = customer.expenses_houses()

    #get expenses
    expenses = customer.all_expenses()

    #get forms and template
    delete_exp_form = Delete_Expense()
    send_data_form = Send_Data()
    template = loader.get_template('expenses/expenses.html')

    context = {
        'houses': houses,
        'expenses': expenses,
        'current_user': current_user,
        'send_data_form': send_data_form,
        'delete_exp_form': delete_exp_form,
    }

    #form logic
    if request.method == 'POST':
        if request.POST.get('delete_exp_form'):
            delete_exp_form = Delete_Expense(request.POST)
            if delete_exp_form.is_valid():

                #POST data
                expense_id = int(request.POST.get('expense_id'))

                #get expense and house
                expense = Expenses.objects.get(pk=expense_id)
                house = expense.house
                expense.delete()

                #set expenses on house to false if no more expenses for that house
                if not Expenses.objects.filter(customer=customer.customer, house=house).exists():
                    house.expenses = False
                    house.save(update_fields=['expenses'])

                return redirect('/expenses/')
    # if a GET (or any other method) we'll create a blank form

    return HttpResponse(template.render(context, request))
