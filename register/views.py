from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from .forms import Register

def register(request):
    current_user = request.user
    form = Register(auto_id=False)
    template = loader.get_template('register/register.html')

    context = {
        'form': form,
    }

    #get the customer id if it exists
    c_id = request.GET.get('c', None)

    #require a link invite from the customer to proceed
    if c_id is not None:
        c_id = str(c_id)
        #form logic
        if request.method == 'POST':
            #get empty form
            form = Register(request.POST)

            if form.is_valid():
                #get data from post
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                #save the user to the database
                user = User.objects.create_user(username, email, password)
                user.save()

                #create the group if it does not exist
                def create_or_get_group(name):
                    if Group.objects.filter(name=name).exists():
                        group = Group.objects.get(name=name)
                    else:
                        group = Group(name=name)
                        group.save()

                    return group

                #determine if the user signing up is staff or a worker
                user_type = request.GET.get('staff', None)

                if user_type is not None:
                    user_group = create_or_get_group('Customers Staff')
                else:
                    user_group = create_or_get_group('Workers')

                customer_group = create_or_get_group(c_id)

                #add user to group
                user.groups.add(user_group, customer_group)

                #login new user
                new_user = authenticate(username=username, password=password)
                login(request, new_user)

                #redirect
                if user_type is not None:
                    return redirect('/payment_requests/approved_payments?new_user=True')
                else:
                    return redirect('/jobs?new_user=True')

        # if a GET (or any other method), we'll create a blank form
        else:
            form = Register(auto_id=False)

        return HttpResponse(template.render(context, request))
    else:
        return redirect('/accounts/login')
