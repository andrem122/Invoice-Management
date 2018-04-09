from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from jobs.models import House
from .forms import Add_House
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.contrib import messages

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def add_house(request):
    current_user = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_House(request.POST)

        if form.is_valid():
            #clean the form data and store into variables
            address = form.cleaned_data['address']

            #handle multiple addresses
            def get_addresses(addresses_string):
                #check if there are multiple addresses
                try:
                    i = addresses_string.index(';')
                except ValueError:
                    return False

                addresses = addresses_string.split(';')
                addresses = (address for address in addresses if address != '') #remove empty elements in the list
                addresses = (address.strip() for address in addresses) #remove trailing white space
                return addresses

            result = get_addresses(address)

            """create the house in the database if it does not exist"""
            if result is not False:
                for r in result:
                    house, created = House.objects.get_or_create(
                        address=r,
                        customer=current_user,
                    )
            else:
                house, created = House.objects.get_or_create(
                    address=address,
                    customer=current_user,
                )

            messages.success(request, 'Thanks! The property has been added.')
            form = Add_House()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_House()

    return render(request, 'add_house/add_house.html', {'form': form})
