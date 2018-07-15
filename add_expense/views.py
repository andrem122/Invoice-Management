from django.shortcuts import render
from .forms import Add_Expense
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.contrib import messages

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def add_expense(request):
    current_user = request.user
    add_expense_form = Add_Expense()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        add_expense_form = Add_Expense(data=request.POST, files=request.FILES)

        if add_expense_form.is_valid():

            house = add_expense_form.cleaned_data['house']
            house.expenses = True
            house.save(update_fields=['expenses'])

            expense = add_expense_form.save(commit=False)
            expense.customer = current_user
            expense.save()

            add_expense_form = Add_Expense()
            messages.success(request, 'Thanks! The expense has been added.')
        else:
            messages.error(request, 'Something went wrong. Please try again.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_Expense()

    return render(
        request,
        'add_expense/add_expense.html',
        {'current_user': current_user, 'add_expense_form': add_expense_form}
    )
