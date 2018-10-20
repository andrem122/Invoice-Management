from django.shortcuts import render, redirect
from jobs.models import House
from .forms import Add_House
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.contrib import messages

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def add_house(request):
    current_user = request.user
    form = Add_House()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_House(data=request.POST)

        if form.is_valid():
            #clean the form data and store into variables
            address = form.cleaned_data['address'].strip() #strip of white space

            house = form.save(commit=False)
            house.customer = current_user
            house.address = address

            #form field handling
            if house.address == '':
                messages.error(request, 'Please enter an address.')
            elif house.purchase_price == 0:
                messages.error(request, 'Please enter a purchase price.')
            elif house.profit == 0:
                messages.error(request, 'Please enter your desired profit.')
            elif house.after_repair_value == 0:
                messages.error(request, 'Please enter the selling price of the property.')
            else:
                house.save()
                messages.success(request, 'Thanks! The property has been added.')
                form = Add_House()
        else:
            messages.error(request, 'Please review the information and try again.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_House()

    return render(request, 'add_house/add_house.html', {'current_user': current_user, 'form': form})
