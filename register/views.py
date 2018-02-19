from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from .forms import Register

def register(request):
    current_user = request.user

    #get the empty forms
    form = Register(auto_id=False)

    template = loader.get_template('register/register.html')

    context = {
        'form': form,
    }

    #get the customer id if it exists
    c_id = str(request.GET.get('c', None))

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
                    group = Group.objects.get(name='Workers')
                else:
                    group = Group(name=name)
                    group.save()

                return group

            worker_group = create_or_get_group('Workers')
            customer_group = create_or_get_group(c_id)


            #add user to group
            user.groups.add(worker_group, customer_group)

            #login new user
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            #redirect
            return redirect('/jobs/?new_user=True')

    # if a GET (or any other method), we'll create a blank form
    else:
        form = Register(auto_id=False)

    return HttpResponse(template.render(context, request))
