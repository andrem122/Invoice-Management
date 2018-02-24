from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from .forms import Customer_Register

def register(request):
    current_user = request.user

    #get the empty form
    form = Customer_Register(auto_id=False)

    #load the template
    template = loader.get_template('customer_register/customer_register.html')

    context = {
        'form': form,
    }

    #form logic
    if request.method == 'POST':
        #get empty form
        form = Customer_Register(request.POST)

        if form.is_valid():
            #get data from post
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            #save the user to the database
            user = User.objects.create_user(username, email, password)
            user.save()

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
                worker_url = 'http://' + request.get_host() + '/register/' + '?c=' + str(user.id)
                staff_url = 'http://' + request.get_host() + '/register/' + '?c=' + str(user.id) + '?staff=True'
                return [worker_url, staff_url]

            urls = generate_urls(request=request, user=user)
            redirect_url = '/jobs_admin/?worker_url=' + urls[0] + '&staff_url=' + urls[1]

            #login new user
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            #redirect
            return redirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Customer_Register(auto_id=False)

    return HttpResponse(template.render(context, request))
