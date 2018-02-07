from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import User

def login(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)

    url = '/jobs'
    user = authenticate(request, username=username, password=password)

    #user is verified
    if user is not None:
        login(request, user)
        redirect(url)
    else:
        return 'Error'

    users = User.objects.all()
    context = {
        'users': users,
    }
    template = loader.get_template('login/login.html')
    response = HttpResponse(template.render(context, request))
    return response
