from django.shortcuts import render
from jobs.models import Job, Request_Payment
from .forms import Add_Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customer_register.customer import Customer
#from optimize_image import optimize_image, is_image, generate_file_path

def is_customer(user):
    """Checks if the current user is a customer"""
    return user.groups.filter(name='Customers').exists()

@login_required
def add_payment(request, job_id):
    current_user = request.user
    form = Add_Payment()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = Add_Payment(data=request.POST, files=request.FILES)

        if form.is_valid():
            #get POST data
            job = Job.objects.get(pk=job_id)
            amount = form.cleaned_data['amount']
            house = job.house

            #check if amount entered is greater than zero
            if int(amount) == 0:
                messages.error(request, 'Please enter an amount greater than zero.')
            else:
                #create new payment object from POST data
                payment = form.save(commit=False)
                payment.amount = amount
                payment.house = house
                payment.job = job
                payment.approved = True

                payment.save()

                messages.success(request, 'Thanks! The payment has been added.')
                form = Add_Payment()
        else:
            messages.error(request, 'Please review the information and try again.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_Payment()

    return render(request, 'add_payment/add_payment.html', {'current_user': current_user, 'form': form})
