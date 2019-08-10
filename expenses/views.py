from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from jobs.models import House
from .models import Expenses
from .forms import Delete_Expense, Edit_Expense
from payment_history.forms import Upload_Document_Form
from jobs_admin.forms import Edit_Job, Approve_Job, Approve_As_Payment, Reject_Estimate
from django.contrib.auth.decorators import user_passes_test
from search_submit.views import Search_Submit_View
from project_management.decorators import customer_and_staff_check
from customer_register.customer import Customer
from ajax.ajax import Ajax

def load_ajax_search_results(request):
    """Loads ajax html for the search view"""
    search_submit_context = {
        'current_user': request.user,
        'query': request.POST.get('query', None),
        'post_from_url': request.POST.get('post_from_url', None),
        'edit_job_form': Edit_Job(user=request.user),
        'edit_expense_form': Edit_Expense(user=request.user),
        'approve_form': Approve_Job(),
        'approve_as_payment_form': Approve_As_Payment(),
        'reject_estimate_form': Reject_Estimate(),
        'upload_document_form': Upload_Document_Form(),
        'delete_exp_form': Delete_Expense(),
    }

    search_submit_view = Search_Submit_View()
    html = search_submit_view.search_results(
        query=search_submit_context.get('query'),
        request=request,
        context=search_submit_context,
        ajax=True)

    return html

def return_html_or_redirect(request, response):
    """
    Returns html if the request is ajax
    or redirects the user if the request is
    not ajax

    Args:
        request: The request object.
        response: The reponse string.

    Returns:
        A HttpResponse object OR a redirect object.

    Raises:
        None.
    """

    if request.is_ajax(): # Ajax requests return HTML as a result, so use HttpResponse
        return HttpResponse(response)
    elif response == '<h2>Error</h2>':
        return HttpResponse(response)
    else:
        return redirect(response)

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
        new_pay_this_week = edit_expense_form.cleaned_data.get('pay_this_week', None)
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
            print('New document file uploaded...')
            expense.document_link = document_link
            expense.save(update_fields=['document_link'])

        if new_description != None:
            expense.description = new_description
            expense.save(update_fields=['description'])

        if new_memo != None:
            expense.memo = new_memo
            expense.save(update_fields=['memo'])

        if new_pay_this_week != None:
            expense.pay_this_week = new_pay_this_week
            expense.save(update_fields=['pay_this_week'])

        if new_amount != None and 1 + float(new_amount) != 1.0:
            expense.amount = new_amount
            expense.save(update_fields=['amount'])

    else:
        print(edit_expense_form.errors)


    if request.is_ajax():
        return load_ajax_search_results(request)
    else:
        return request.POST.get('post_from_url', None)

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def expenses(request):
    customer = Customer(request.user)

    # Handle HTTP requests
    response = '<h2>Error</h2>'
    # POST requests
    if request.method == 'POST':
        if request.POST.get('delete_exp_form', None) != None:
            response = delete_expense(request, customer)
        elif request.POST.get('edit_expense', None) != None:
            response = edit_expense(request, customer)

        return return_html_or_redirect(request, response)

    else: # GET or any other method
        return return_html_or_redirect(request, response)
