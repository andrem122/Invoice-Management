from django.shortcuts import render, redirect
from jobs.models import House
from .forms import Add_House
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.contrib import messages
from io import TextIOWrapper
import csv
import pandas as pd
import os

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def add_house(request):
    current_user = request.user
    form = Add_House()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_House(data=request.POST, files=request.FILES)

        if form.is_valid():
            #clean the form data and store into variables
            address = form.cleaned_data['address'].strip() #strip of white space
            house_list_file = form.cleaned_data['house_list_file']

            #handle multiple addresses in a single string
            def add_addresses(address_string):
                if address_string != '':
                    try:
                        index = address_string.index(';')
                    except ValueError:
                        index = False

                    #if no multiple addresses in the string, then add the one address
                    if index == False:
                        house, created = House.objects.get_or_create(
                            address=address_string,
                            customer=current_user,
                        )
                        """
                        first value is True because the data was added. Second value
                        is False because it was NOT a multiple address string
                        """
                        return (True, False)

                    addresses = address_string.split(';')
                    addresses = (address for address in addresses if address != '') #remove empty elements in the list
                    addresses = (address.strip() for address in addresses) #remove trailing white space

                    #add multiple addresses to database
                    for address in addresses:
                        house, created = House.objects.get_or_create(
                            address=address,
                            customer=current_user,
                        )

                    return (True, True)
                else:
                    messages.error(request, 'Please enter an address or upload a file.')
                    return (False, False)

            #gets addresses from an uploaded csv file
            def write_addresses_from_file(house_list_file):
                if len(request.FILES) != 0:
                    file_name = house_list_file.name
                    #check file extension and convert to csv if needed
                    if file_name.lower().endswith('.xlsx'):
                        df = pd.read_excel(house_list_file, sheetname=0, index_col=False, skip_blank_lines=True)
                        df.to_csv(file_name, encoding='utf-8')
                    elif file_name.lower().endswith('.csv'):
                        df = pd.read_csv(house_list_file)
                    else:
                        messages.error(request, 'Please upload a CSV or Excel file.')
                        return False
                    #check for address column
                    columns = [column.lower().strip() for column in df.columns]
                    try:
                        index = columns.index('address')
                    except ValueError as e:
                        messages.error(request, 'Add "address" as a header for the address column in your spreadsheet.')
                        return False
                    #convert data to strings
                    addresses = (str(address) for address in df.iloc[:, index])
                    addresses = (address.strip() for address in addresses) #remove trailing white space
                    for address in addresses:
                        house, created = House.objects.get_or_create(
                            address=address,
                            customer=current_user,
                        )
                    return True
                else:
                    messages.error(request, 'Please upload a CSV or Excel file.')

            """Add to Database"""
            #text input and a file input
            if address != '' and len(request.FILES) != 0:
                #add the houses in the uploaded file and text input
                file_addresses_added = write_addresses_from_file(house_list_file=house_list_file)

                #check if addresses from the file were uploaded
                if file_addresses_added == True:
                    addresses_added = add_addresses(address)
                    #check if addresses from input text were added
                    if True in addresses_added:
                        messages.success(request, 'Thanks! The properties have been added.')
                form = Add_House()
            #file input only
            elif len(request.FILES) != 0:
                if write_addresses_from_file(house_list_file=house_list_file):
                    messages.success(request, 'Thanks! The properties have been added.')
            #text input only
            else:
                addresses_added = add_addresses(address)
                if False not in addresses_added:
                    messages.success(request, 'Thanks! The properties have been added.')
                if addresses_added[0] == True and addresses_added[1] == False:
                    messages.success(request, 'Thanks! The property has been added.')

                form = Add_House()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_House()

    return render(request, 'add_house/add_house.html', {'current_user': current_user, 'form': form})
