from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from jobs.models import Job, House
from .forms import AddJob, AddJob_Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customer_register.customer import Customer
from project_management.decorators import worker_check
from optimize_image import optimize_image, is_image, generate_file_path

def is_customer(user):
    """Checks if the current user is a customer"""
    return user.groups.filter(name='Customers').exists()

@login_required
def add_job(request):
    current_user = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        if is_customer(current_user):
            form = AddJob_Customer(data=request.POST, files=request.FILES, user=current_user)
        else:
            form = AddJob(data=request.POST, files=request.FILES, user=current_user)

        if form.is_valid():

            #clean the form data and store into variables
            #variables for the Job instance
            house = form.cleaned_data['house']

            if is_customer(current_user):
                company = form.cleaned_data['company']

            start_amount = form.cleaned_data['start_amount']
            img_names = (form.cleaned_data['document_link'].name, )

            #the house now has a proposed job, so set proposed_jobs=True
            house.proposed_jobs=True
            house.save(update_fields=['proposed_jobs'])

            #save the uploaded file and the job
            job = form.save(commit=False)

            if is_customer(current_user):
                job.company = company
            else:
                job.company = current_user

            job.approved = False
            job.save()

            result = is_image(img_names)
            if result == True:
                file_paths = generate_file_path(house=house, img_names=img_names, upload_folder='worker_uploads')
                optimize_image(file_paths)

            messages.success(request, 'Thanks! Your job was submitted and is awaiting approval.')

            if is_customer(current_user):
                form = AddJob_Customer(user=current_user)
                return render(request, 'addjob/addjob_customer.html', {'form': form, 'current_user': current_user})
            else:
                form = AddJob(user=current_user)
                return render(request, 'addjob/addjob.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        if is_customer(current_user):
            form = AddJob_Customer(user=current_user)
            return render(request, 'addjob/addjob_customer.html', {'form': form, 'current_user': current_user})
        else:
            form = AddJob(user=current_user)
            return render(request, 'addjob/addjob.html', {'form': form})
