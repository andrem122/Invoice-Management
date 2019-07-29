from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import House, Job
from .forms import Request_Payment_Form
from django.contrib.auth.decorators import user_passes_test, login_required
from project_management.decorators import worker_check
from register.worker import Worker
from customer_register.models import Customer_User
from itertools import chain
from optimize_image import optimize_image, is_image, generate_file_path

def generate_login_url(request):
    protocol = 'http://'
    if request.is_secure():
        protocol = 'https://'

    return protocol + request.get_host() + '/accounts/login/'

@user_passes_test(worker_check, login_url='/accounts/login/')
def index(request):
    current_user = request.user

    worker = Worker(current_user)
    approved_houses = worker.approved_houses()
    unapproved_houses = worker.current_week_unapproved_houses()
    completed_houses = worker.current_week_completed_houses()

    active_jobs = worker.active_jobs()
    unapproved_jobs = worker.current_week_unapproved_jobs()
    completed_jobs = worker.current_week_completed_jobs()

    print(active_jobs)

    houses = set(chain(approved_houses, unapproved_houses, completed_houses))
    items = set(chain(active_jobs, unapproved_jobs, completed_jobs))

    template = loader.get_template('jobs/index.html')
    request_payment_form = Request_Payment_Form()

    context = {
        'houses': houses,
        'items': items,
        'current_user': current_user,
        'request_payment_form': request_payment_form,
        'login_url': generate_login_url(request),
    }

    #check if the user is new to send a welcome message
    new_user = request.GET.get('new_user')

    if new_user:
        context['new_user'] = new_user
        context['login_url'] = generate_login_url(request)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        request_payment_form = Request_Payment_Form(data=request.POST, files=request.FILES)

        if request_payment_form.is_valid():
            #get job ID from POST
            job_id = int(request.POST.get('job_id'))

            #clean the form data and store into variables
            job = Job.objects.get(pk=job_id)
            house = job.house
            amount = request_payment_form.cleaned_data['amount']
            img_names = (request_payment_form.cleaned_data['document_link'].name, )

            payment = request_payment_form.save(commit=False)
            payment.job = job
            payment.house = house
            payment.requested_by_worker=True
            payment.save()

            if not House.objects.filter(pk=house.pk, pending_payments=True).exists():
                house.pending_payments = True
                house.save(update_fields=['pending_payments'])

            result = is_image(img_names)
            if result == True:
                file_paths = generate_file_path(house=house, user=current_user, img_names=img_names, upload_folder='worker_uploads')
                optimize_image(file_paths)

            return redirect('/jobs/thank_you')
        else:
            print(request_payment_form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        request_payment_form = Request_Payment_Form()

    return HttpResponse(template.render(context, request))

@login_required
def thank_you(request):
    template = loader.get_template('jobs/thank_you.html')
    return HttpResponse(template.render(request=request))

#redirect a user after successful login
def redirect_user(request):
    if request.user.groups.filter(name='Customers').exists(): #if the user is a customer
        customer, created = Customer_User.objects.get_or_create(user=request.user)
        return redirect('/jobs-admin/')
    elif request.user.groups.filter(name='Customers Staff').exists(): #if the user is customer's staff
        return redirect('/payments')
    elif request.user.is_superuser:
        return redirect('/admin')
    else:
        return redirect('/jobs')
