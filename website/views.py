from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from website.forms import Contact_Sales, Contact_Support
from django.core.mail import send_mail
from django.contrib import messages

def home(request):
    #load the template
    template = loader.get_template('website/home.html')
    context = {}

    return HttpResponse(template.render(context, request))

def product(request):
    #load the template
    template = loader.get_template('website/product.html')
    context = {}

    return HttpResponse(template.render(context, request))

def contact_sales(request):
    #load the template
    template = loader.get_template('website/contact_sales.html')
    contact_sales_form = Contact_Sales()
    context = {
        'contact_sales_form': contact_sales_form,
    }

    if request.method == 'POST':
        contact_sales_form = Contact_Sales(data=request.POST)
        if contact_sales_form.is_valid():
            first_name = contact_sales_form.cleaned_data['first_name']
            last_name = contact_sales_form.cleaned_data['last_name']
            email = contact_sales_form.cleaned_data['email']
            phone_number = contact_sales_form.cleaned_data['phone_number']

            message = """
            A demo of Nova One has been requested.\n
            First Name: {first_name}\n
            Last Name: {last_name}\n
            Email: {email}\n
            Phone Number: {phone_number}
            """.format(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )

            send_mail(
                'Demo Requested',
                message,
                'no-reply@novaonesoftware.com',
                ['andre.mashraghi@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, 'Thanks! Your demo request has been sent!')
        else:
            messages.error(request, 'Validation Error: Please try again.')
    else:
        contact_sales_form = Contact_Sales()
    return HttpResponse(template.render(context, request))

def contact_support(request):
    if request.method == 'POST':
        contact_support_form = Contact_Support(data=request.POST)
        if contact_support_form.is_valid():
            email = contact_support_form.cleaned_data['email']
            form_message = contact_support_form.cleaned_data['message']

            email_message = """
            A customer has requested support. Please see details below.\n
            Customer Email: {email}\n
            Customer Message: {form_message}
            """.format(
                email=email,
                form_message=form_message,
            )

            send_mail(
                'Customer Support Needed',
                email_message,
                'no-reply@novaonesoftware.com',
                ['andre.mashraghi@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, 'Thanks! Your message has been sent!')
        else:
            messages.error(request, 'Validation Error: Please try again.')
    else:
        raise Http404("Invalid request: Only POST request allowed.")

    template = loader.get_template('404.html')
    return HttpResponse(template.render(request=request))

def privacy_policy(request):
    #load the template
    template = loader.get_template('website/privacy_policy.html')
    context = {}

    return HttpResponse(template.render(context, request))

def terms_and_conditions(request):
    #load the template
    template = loader.get_template('website/terms_and_conditions.html')
    context = {}

    return HttpResponse(template.render(context, request))
