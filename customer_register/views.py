from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import Customer_User
from django.contrib.auth import authenticate, login
from .forms import User_Register, Customer_User_Register

def register(request):
    current_user = request.user

    #get the empty form
    user_register_form = User_Register(auto_id=False)
    customer_user_form = Customer_User_Register()

    #load the template
    template = loader.get_template('customer_register/customer_register.html')

    context = {
        'user_register_form': user_register_form,
        'customer_user_form': customer_user_form,
    }

    #form logic
    if request.method == 'POST':
        #get empty form
        user_register_form = User_Register(request.POST)
        customer_user_form = Customer_User_Register(request.POST)

        if user_register_form.is_valid() and customer_user_form.is_valid():

            #get data from post
            username = user_register_form.cleaned_data['username']
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            phone_number = customer_user_form.cleaned_data['phone_number']

            #create user and save to the database
            user = User.objects.create_user(username, email, password)
            customer_user = Customer_User.objects.create(
                user=user,
                is_paying=False,
                phone_number=phone_number.as_e164,
            )

            user.save()
            customer_user.save()

            #create the Customers group if it does not exist
            if Group.objects.filter(name='Customers').exists():
                group = Group.objects.get(name='Customers')
            else:
                group = Group(name='Customers')
                group.save()

            #add user to group
            user.groups.add(group)

            #generate url for customer to send to workers and staff to sign up
            def generate_urls(request, user):
                if request.is_secure():
                    protocol = 'https://'
                else:
                    protocol = 'http://'

                worker_url = protocol + request.get_host() + '/register/' + '?c=' + str(user.id)
                staff_url = protocol + request.get_host() + '/register/' + '?c=' + str(user.id) + '?staff=True'
                return [worker_url, staff_url]

            urls = generate_urls(request=request, user=user)
            redirect_url = '/jobs-admin/?worker_url=' + urls[0] + '&staff_url=' + urls[1]

            #login new user
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            #redirect
            return redirect(redirect_url)
        else:
            print(user_register_form.errors)
            print(customer_user_form.errors)
    # if a GET (or any other method) we'll create a blank form
    else:
        user_register_form = User_Register(auto_id=False)
        customer_user_form = Customer_User_Register()

    return HttpResponse(template.render(context, request))
