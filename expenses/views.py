from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from jobs.models import House
from .models import Expenses
from .forms import Delete_Expense, Edit_Expense
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from customer_register.customer import Customer

def delete_expense(request, customer):
    # Handles POST requests to delete an expense object
    if request.POST.get('delete_exp_form', None) != None:
        delete_exp_form = Delete_Expense(request.POST)
        if delete_exp_form.is_valid():

            # POST data
            expense_id = int(request.POST.get('expense_id'))
            post_from_url = request.POST.get('post_from_url')

            # Get expense and house
            expense = Expenses.objects.get(pk=expense_id)
            house = expense.house
            expense.delete()

            # Set expenses on house to false if no more expenses for that house
            if not Expenses.objects.filter(customer=customer.customer, house=house).exists():
                house.expenses = False
                house.save(update_fields=['expenses'])

            return post_from_url

def edit_expense(request, customer):
    """
    Called when a user edits an expense's properties
    """
    expense_id = int(request.POST.get('expense_id')) #get expense id from POST request
    expense = get_object_or_404(Expenses, id=expense_id) #get expense instance
    post_from_url = request.POST.get('post_from_url', None)

    edit_expense_form = Edit_Expense(data=request.POST, files=request.FILES, user=request.user)

    if edit_expense_form.is_valid():

        previous_house = expense.house #the house the expense object belonged to before it is changed
        new_house = edit_expense_form.cleaned_data.get('house', None)
        new_amount = edit_expense_form.cleaned_data.get('amount', None)
        new_expense_type = edit_expense_form.cleaned_data.get('expense_type', None)
        pay_this_week = edit_expense_form.cleaned_data.get('pay_this_week', None)
        new_description = edit_expense_form.cleaned_data.get('description', None)
        new_memo = edit_expense_form.cleaned_data.get('memo', None)
        document_link = edit_expense_form.cleaned_data.get('document_link', None)
        print(edit_expense_form.cleaned_data)

        #update the expense instance based on which fields were submitted in the form
        if new_house != None:
            expense.house = new_house

            #update object
            expense.save(update_fields=['house'])

        if new_expense_type != None:
            #change and save new job type on job object
            expense.expense_type = new_expense_type
            expense.save(update_fields=['expense_type'])

        if document_link != None:
            expense.document_link = document_link
            expense.save(update_fields=['document_link'])

        if new_description != None:
            expense.description = new_description
            expense.save(update_fields=['description'])

        if new_memo != None:
            expense.memo = new_memo
            expense.save(update_fields=['memo'])

        if new_amount != None and 1 + float(new_amount) != 1.0: #update balance_amount if amount is in the POST data
            expense.amount = new_amount
            expense.save(update_fields=['amount'])

    else:
        print(edit_expense_form.errors)


    # if request.is_ajax():
    #     if 'search' in post_from_url:
    #         return load_ajax_search_results(request)
    #     else:
    #         ajax = Ajax(customer)
    #         html = ajax.load_ajax_results('jobs')
    #         return html
    # else:
    #     return request.POST.get('post_from_url', None)

    return request.POST.get('post_from_url', None)

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def expenses(request):
    customer = Customer(request.user)

    # POST requests
    response = '<h2>Error</h2>'
    if request.method == 'POST':
        if request.POST.get('delete_exp_form', None) != None:
            response = delete_expense(request, customer)
        elif request.POST.get('edit_expense', None) != None:
            response = edit_expense(request, customer)

    if response == '<h2>Error</h2>':
        return HttpResponse(response)
    else:
        return redirect(response)
