from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from jobs.models import House
from .forms import Add_House
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.contrib import messages
from io import TextIOWrapper
import csv

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def add_house(request):
    current_user = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_House(data=request.POST, files=request.FILES)

        if form.is_valid():
            #clean the form data and store into variables
            address = form.cleaned_data['address']
            house_list_file = form.cleaned_data['house_list_file']

            #handle multiple addresses in a single string
            def get_addresses(addresses_string):
                try:
                    i = addresses_string.index(';')
                except ValueError:
                    return False

                addresses = addresses_string.split(';')
                addresses = (address for address in addresses if address != '') #remove empty elements in the list
                addresses = (address.strip() for address in addresses) #remove trailing white space
                return addresses

            addresses = get_addresses(address)

            #gets addresses from an uploaded csv file
            def get_addresses_from_file(house_list_file):
                #change encoding to UTF-8
                csvfile = TextIOWrapper(house_list_file.file, encoding=request.encoding)
                #find these strings in the columns of the csv file
                find = 'address'
                reader = csv.reader(csvfile)
                columns = next(reader)
                columns = (column_name.lower().strip() for column_name in columns)

                #find column with the addresses
                for i, column in enumerate(columns):
                    print(column)
                    index = None
                    if column == find:
                        index = i
                        break
                print(index)
                #if address column was not found
                if index == None:
                    messages.error(request, 'Add "address" as a header for the address column in your spreadsheet.')
                    form = Add_House()
                    return

                #get column with the addresses
                for line in reader:
                    if line[index] != '':
                        house, created = House.objects.get_or_create(
                            address=line[index],
                            customer=current_user,
                        )

                messages.success(request, 'Thanks! The properties have been added.')

            """create the house in the database if it does not exist"""
            if addresses is not False and len(request.FILES) != 0:
                #add the multiple addresses parsed from the input string
                for address in addresses:
                    house, created = House.objects.get_or_create(
                        address=address,
                        customer=current_user,
                    )
                #add the houses in the uploaded file
                get_addresses_from_file(house_list_file=house_list_file)
                messages.success(request, 'Thanks! The properties have been added.')
            elif len(request.FILES) != 0:
                get_addresses_from_file(house_list_file=house_list_file)
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
