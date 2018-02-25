from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from jobs.models import House
from .forms import Add_House
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_house(request):
    current_user = request.user
    if current_user.is_active and current_user.groups.filter(name__in=['Customers']).exists():
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = Add_House(request.POST)

            if form.is_valid():
                #clean the form data and store into variables
                address = form.cleaned_data['address']

                """update or create the house in the database"""
                house, created = House.objects.get_or_create(
                    address=address,
                    customer=current_user,
                )

                messages.success(request, 'Thanks! The property has been added.')
                form = Add_House()

        # if a GET (or any other method) we'll create a blank form
        else:
            form = Add_House()
    else:
        return HttpResponseRedirect('/accounts/login')

    return render(request, 'add_house/add_house.html', {'form': form})
