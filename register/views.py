from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import Register

def register(request):
    #get all houses that currently have workers working on them
    current_user = request.user

    #get the empty forms
    form = Register(auto_id=False)

    template = loader.get_template('register/register.html')

    context = {
        'form': form,
    }

    #form logic
    if request.method == 'POST':
        #get empty form
        form = Register(request.POST)

        if form.is_valid():
            #get data from post
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            #save the form
            user = User.objects.create_user(username, email, password)
            user.save()

            #redirect
            return HttpResponseRedirect('/accounts/login')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Register(auto_id=False)

    return HttpResponse(template.render(context, request))
