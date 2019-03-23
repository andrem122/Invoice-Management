from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def home(request):
    #load the template
    template = loader.get_template('website/home.html')
    context = {}

    return HttpResponse(template.render(context, request))
